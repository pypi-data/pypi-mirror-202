# -*- coding: utf-8 -*-
""" API module for Exbet Market Making API
"""
import time
import requests
from inspect import signature
from requests.auth import AuthBase
from .exceptions import (
    JsonDecodingFailedException,
    AlreadyLoggedinException,
    ExecutionError,
    APIError,
)


class ExbetAPIAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


class ExbetAPI:
    """API Class for Market Making"""

    BASEURL = "https://api.macau.exbet.io/"

    _SLEEPTIME = 0.2
    _BLOCKTIME = 1

    def __init__(self, *args, **kwargs):
        if kwargs.pop("use_everett", None):
            self.BASEURL = "https://api.everett.exbet.io/"
        if "use_url" in kwargs:
            self.BASEURL = kwargs.pop("use_url")
        vars(self).update(**kwargs)

        self.__requests_obj = None
        self.__requests_auth = None

    @property
    def _requests(self):
        """Returns a requets session"""
        # Cache the session for keep-alive
        if self.__requests_obj is None:
            self.__requests_obj = requests.Session()
            # Update headers
            self.__requests_obj.headers.update(self._headers())
        # Ensure we authenticate if logged-in
        if self.__requests_auth:
            self.__requests_obj.auth = self.__requests_auth
        return self.__requests_obj

    def _headers(self):
        """Provides header for POST and GET requests"""
        from . import __version__

        headers = dict()
        headers["User-Agent"] = "python/exbetapi-" + __version__
        return headers

    def _post(self, endpoint: str, payload: dict) -> dict:
        """Private method to send a POST request with payload to the API"""
        assert isinstance(payload, dict)
        resp = self._requests.post(self.BASEURL + endpoint, json=payload)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            try:
                t = resp.json()
            except Exception:
                t = resp.text
            raise APIError(t)
        try:
            ret = resp.json()
        except Exception:  # pragma: no cover
            raise JsonDecodingFailedException("Decoding API response failed!")
        ret = self._parse_response(ret)
        return ret

    def _get(self, endpoint: str) -> dict:
        """Private method to send a GET from API resource"""
        resp = self._requests.get(self.BASEURL + endpoint)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            try:
                t = resp.json()
            except Exception:
                t = resp.text
            raise APIError(t)
        try:
            ret = resp.json()
        except Exception:  # pragma: no cover
            raise JsonDecodingFailedException("Decoding API response failed!")
        ret = self._parse_response(ret)
        return ret

    @staticmethod
    def _parse_response(ret):
        """We parse the response for exceptions/errors that the API returns"""
        if "error" in ret:  # pragma: no cover
            raise APIError([x["message"] for x in ret["errors"]])
        return ret

    @staticmethod
    def _require_dict_keys(resp: dict, attributes: list) -> None:
        """Internal test for required dict keys"""
        assert all([x in resp for x in attributes])

    def _get_task(self, task_id: str) -> dict:
        """Obtain a task from the API"""
        return self._post("v2/task", dict(task_id=task_id))

    def _wait_for_task(self, task_id: str) -> dict:  # pragma: no cover
        """Wait for a task to complete"""
        cnt = 0
        while True:
            task = self._get_task(task_id)
            if (
                task.get("ready")
                and task.get("state") == "SUCCESS"
                and task.get("info")
            ):
                task["info"] = eval(task.get("info", "{}"))
                return task
            time.sleep(self._SLEEPTIME)
            cnt += 1
            if cnt > 3 * self._BLOCKTIME / self._SLEEPTIME:
                raise ExecutionError(f"Inform admins {task_id}: {str(task)}")

    @staticmethod
    def _obtain_task_results(task):  # pragma: no cover
        """A task contains information about the operations performed. Extract
        those
        """
        results = task["info"].get("operation_results")
        if results:
            return [x[1] for x in results]
        return []

    @staticmethod
    def _parse_stake(stake):
        """Stake cane be provided as string and dictionary. Unified here."""
        if isinstance(stake, str) and " " in stake:
            amount, symbol = stake.split(" ")
            return dict(amount=float(amount), symbol=symbol)
        if isinstance(stake, dict) and "amount" in stake and "symbol" in stake:
            return dict(amount=float(stake["amount"]), symbol=stake["symbol"])
        raise ValueError("Invalid stake format")  # pragma: no cover

    #
    # Public methods
    #
    def reset(self):
        """Reset instance"""
        self.__requests_auth = None

    def login(self, username: str, password: str) -> None:
        """Obtain and store session for user"""
        if self.__requests_auth is not None:
            raise AlreadyLoggedinException("Reset instance with .reset()")
        resp = self._post("v2/login", dict(username=username, password=password))
        self._require_dict_keys(resp, ["access_token", "refresh_token", "username"])
        self.__requests_auth = ExbetAPIAuth(resp["access_token"])

    #
    # General information
    #
    def is_loggedin(self) -> bool:
        """Am i logged in?"""
        return bool(self.__requests_auth)

    @property
    def info(self) -> dict:
        """Obtain general information from the API"""
        return self._get("v2/info")

    @property
    def session(self) -> dict:
        """Obtain session information"""
        return self._get("v2/session")

    #
    # Account information
    #
    @property
    def account(self) -> dict:
        """Obtain account details"""
        return self._get("v2/account")

    @property
    def balance(self) -> dict:
        """Obtain account balance from api"""
        balances = self._get("v2/balance").get("balances")
        ret = dict()
        for b in balances:
            ret[b["symbol"]] = b["amount"]
        return ret

    @property
    def roles(self) -> list:
        """Provide roles of the account"""
        return self.account.get("roles")

    def wait_for_task(func):
        def func_wrapper(self, *args, **kwargs):
            resp = func(self, *args, **kwargs)
            wait_kwarg = signature(func).parameters["wait"].default or kwargs.pop(
                "wait", False
            )
            if wait_kwarg:
                self._wait_for_task(resp.get("task_id"))
            return resp

        return func_wrapper

    #
    # Bets
    #
    def get_bet(self, bet_id: str) -> dict:
        """Obtain details of a placed bet

        :param str bet_id: Bet of the form ``1.26.xxxxxxx``
        """
        return self._post("v2/bet/get", dict(bet_id=bet_id))

    def list_bets(self) -> dict:
        """List account's bets, sorted for matched and unmatched"""
        return self._get("v2/bet/list")

    def list_matched(self) -> dict:
        """List account's matched bets"""
        return self._post("v2/bet/list_matched")

    def list_unmatched(self) -> dict:
        """List account's unmatched bets"""
        return self._post("v2/bet/list_unmatched")

    @wait_for_task
    def many_actions(self, actions: dict, wait=False) -> None:
        """Perform many edits, cancels and places at the same time"""
        return self._post("v2/bet/many_actions", actions)

    @wait_for_task
    def cancel_bet(self, bet_id: str, wait=False) -> None:
        """
        :param str bet_id: Bet of the form ``1.26.xxxxxxx``
        :param bool wait: Wait/Block until action has been confirmed
        """
        return self._post("v2/bet/cancel", dict(bet_id=bet_id))

    @wait_for_task
    def cancel_bets(self, bet_ids: list, wait=False) -> None:
        """
        :param list bet_ids: List of bets of the form ``1.26.xxxxxxx``
        :param bool wait: Wait/Block until action has been confirmed
        """
        return self._post(
            "v2/bet/cancel_many",
            dict(bets_to_cancel=[dict(bet_id=bet_id) for bet_id in bet_ids]),
        )

    @wait_for_task
    def edit_bet(self, new_bet: dict, wait=False):
        """Edit single bet"""
        return self._post("v2/bet/edit", new_bet)

    @wait_for_task
    def edit_bets(self, new_bets: dict, wait=False):
        """Edit multiple bets"""
        return self._post("v2/bet/edit_many", new_bets)

    @wait_for_task
    def modify_unmatched(self, bet_to_modify: dict, wait=False):
        return self._post("v2/bet/modify_unmatched", bet_to_modify)

    @wait_for_task
    def modify_unmatched_many(self, bets_to_modify: dict, wait=False):
        return self._post("v2/bet/modify_unmatched_many", bets_to_modify)

    def place_bet(
        self,
        selection_id: str,
        back_or_lay: str,
        backer_multiplier: float,
        stake: dict,
        persistent=True,
        wait=False,
    ) -> dict:
        """Place a bet

        :param str selection_id: The selection id to place the bet in (1.25.xxxx)
        :param option back_or_lay: Either 'back' or 'lay' the bet
        :param float backer_multiplier: Odds
        :param str stake: Stake as ``amount symbol``
        :param bool persistent: Make the bet persistent over status change from
            upcoming to in_progress
        :param bool wait: Wait for confirmation of the database (if `true`
            returns `bet_id`, else returns `None`).

        Example:::

            bet_id = api.place_bet("1.25.50449", "lay", 1.65, "0.01 BTC", wait=True)

        """
        stake = self._parse_stake(stake)
        resp = self._post(
            "v2/bet/place",
            dict(
                back_or_lay=back_or_lay,
                selection_id=selection_id,
                backer_multiplier=backer_multiplier,
                persistent=persistent,
                backer_stake=stake,
            ),
        )
        if wait:  # pragma: no cover
            return self._obtain_task_results(self._wait_for_task(resp.get("task_id")))
        return resp

    def place_bets(self, bets: list, wait=False) -> list:
        """Place multiple bets

        :param list bets: This is a list in the form of `place_bet` arguments.
        :param bool wait: Wait for confirmation of the database (if `true`
                returns `bet_id`, else returns `None`).

        Example:::

            api.place_bets(
                [
                    ("1.25.50449", "lay", 1.65, "0.01 BTC"),
                    ("1.25.50449", "back", 1.75, "0.01 BTC"),
                ],
                wait=True,
            )

        """
        parsed_bets = list()
        for bet in bets:
            b = dict(
                selection_id=bet[0],
                back_or_lay=bet[1],
                backer_multiplier=bet[2],
                backer_stake=self._parse_stake(bet[3]),
                persistent=True,
            )
            if len(bet) > 4:
                b["persistent"] = bet[4]
            parsed_bets.append(b)
        resp = self._post("v2/bet/place_many", dict(place_bets=parsed_bets))
        if wait:  # pragma: no cover
            return self._obtain_task_results(self._wait_for_task(resp.get("task_id")))
        return resp

    #
    # Find
    #
    def find_selection(
        self, sport: str, event_group: str, teams: dict, market: str, selection: str
    ):
        """Find a selection id provided sufficient information

        :param str sport: Sports name (e.g. Basketball)
        :param str event_group: Name of the event group (e.g. NBA)
        :param dict teams: dictionary in the form of ``{"home": "xx", "away": "yy"}``
        :param str market: Market name (e.g. Moneyline)
        :param str selection: The individual selection name (e.g. "xx" for Team xx)

        """
        return self._post(
            "v2/find/selections",
            dict(
                sport=sport,
                event_group=event_group,
                teams=teams,
                market=market,
                selection=selection,
            ),
        )

    def find_recognized_selection(self) -> dict:
        return self._get("v2/find/selections/recognized")

    #
    # Lookup
    #
    def lookup_selection(self, selection_id: str) -> dict:
        """Provides information about a selection

        :param str selection_id: The selection id (1.25.xxx)
        """
        return self._post("v2/lookup/selection", dict(selection_id=selection_id))

    def lookup_selections(self, market_id: str) -> dict:
        """
        Provides a list of selections in a market

        :param str market_id: Market id (1.24.xxxx)
        """
        return self._post(
            "v2/lookup/selections",
            dict(market_id=market_id),
        ).get("selections")

    def lookup_market(self, market_id: str) -> dict:
        """Provides information about a market

        :param str market_id: Market  id (1.24.xxxx)
        """
        return self._post(
            "v2/lookup/market",
            dict(market_id=market_id),
        )

    def lookup_markets(self, event_id: str) -> list:
        """
        List markets of an event

        :param str event_id: Event id (1.22.xxx)
        """
        return self._post("v2/lookup/markets", dict(event_id=event_id)).get("markets")

    def lookup_event(self, event_id: str) -> dict:
        """Provide information about an event

        :param str event_id: Event id (1.22.xxx)

        """
        return self._post("v2/lookup/event", dict(event_id=event_id))

    def lookup_upcoming_events(self, event_parameters: dict) -> dict:
        return self._post("v2/lookup/events_upcoming", event_parameters)

    def lookup_events(self, eventgroup_id: str) -> list:
        """List events within an event group

        :param str eventgroup_id: Event Group id (1.21.xxx)
        """
        return self._post("v2/lookup/events", dict(eventgroup_id=eventgroup_id)).get(
            "events"
        )

    def lookup_eventgroups(self, sport_id: str) -> list:
        """List event groups with a sport

        :param str sport_id: Sport id (1.20.xxx)
        """
        return self._post("v2/lookup/eventgroups", dict(sport_id=sport_id)).get(
            "eventgroups"
        )

    def lookup_sports(self) -> list:
        """List all sports"""
        return self._post("v2/lookup/sports", dict()).get("sports")

    #
    # Orderbook
    #
    def orderbook(self, selection_id: str) -> dict:
        """Provide (consolidated) order book of a selection

        :param str selection_id: The selection id (1.25.xxx)
        """
        return self._post("v2/lookup/orderbook", dict(selection_id=selection_id))

    def orderbooks(self, market_ids: dict) -> dict:
        return self._post("v2/lookup/orderbook_many", market_ids)

    def spread_place_bets(
        self,
        spread_bets: list,
        wait=False,
    ) -> dict:
        """
        Place a list of bets, with each bet being a dict consisting of

            str selection_id: The selection id to place the bet in (1.25.xxxx)
            option back_or_lay: Either 'back' or 'lay' the bet
            float backer_multiplier: Odds
            str stake_per_unit: Stake as ``amount symbol``
            bool persistent: Make the bet persistent over status change from
            upcoming to in_progress

        :param list spread_bets: List of the bets to place
        :param bool wait: Wait for confirmation of the database (if `true`
            returns `bet_id`, else returns `None`)

        Example:::

            bet_id = api.spread_place_bets(
                [
                    dict(
                        selection_id="1.25.50449",
                        buy_or_sell="buy",
                        price=1.65,
                        stake_per_unit="0.01 USDT"
                    )
                ],
                wait=True
            )

        """
        for spread_bet in spread_bets:
            spread_bet["stake_per_unit"] = self._parse_stake(
                spread_bet["stake_per_unit"]
            )
        resp = self._post(
            "v3/spread-betting/bets",
            dict(bets=spread_bets),
        )
        if wait:  # pragma: no cover
            return self._obtain_task_results(self._wait_for_task(resp.get("task_id")))
        return resp

    def spread_place_bet(
        self,
        selection_id: str,
        buy_or_sell: str,
        price: float,
        stake_per_unit: dict,
        persistent=True,
        wait=False,
    ) -> dict:
        """Place a bet

        :param str selection_id: The selection id to place the bet in (1.25.xxxx)
        :param option back_or_lay: Either 'back' or 'lay' the bet
        :param float backer_multiplier: Odds
        :param str stake_per_unit: Stake as ``amount symbol``
        :param bool persistent: Make the bet persistent over status change from
            upcoming to in_progress
        :param bool wait: Wait for confirmation of the database (if `true`
            returns `bet_id`, else returns `None`).
        """
        self.spread_place_bets(
            [
                dict(
                    selection_id=selection_id,
                    buy_or_sell=buy_or_sell,
                    price=price,
                    stake_per_unit=stake_per_unit,
                    persistent=persistent,
                )
            ],
            wait=wait,
        )

    def spread_orderbook(self, selection_id: str) -> dict:
        """Provide (consolidated) order book of a selection

        :param str selection_id: The selection id (1.25.xxx)
        """
        return self._get(f"v3/spread-betting/orderbooks/{selection_id}")["orderbooks"][
            0
        ]

-module({{name}}).
-behaviour(cloudi_service).

%% cloudi_service callbacks
-export([cloudi_service_init/4,
         cloudi_service_handle_request/11,
         cloudi_service_handle_info/3,
         cloudi_service_terminate/3]).

-include_lib("cloudi_core/include/cloudi_logger.hrl").

-record(state,
    {
    }).

cloudi_service_init(_Args, _Prefix, _Timeout, Dispatcher) ->
    cloudi_service:subscribe(Dispatcher, "{{name}}/get"),
    {ok, #state{}}.

cloudi_service_handle_request(_RequestType, _Name, _Pattern,
                              _RequestInfo, _Request,
                              _Timeout, _Priority,
                              _TransId, _Pid,
                              #state{} = State, _Dispatcher) ->
    Response = cloudi_x_jsx:encode([{<<"status">>, <<"ok">>}]),
    {reply, Response, State}.

cloudi_service_handle_info(Request, State, _Dispatcher) ->
    ?LOG_WARN("Unknown info \"~p\"", [Request]),
    {noreply, State}.

cloudi_service_terminate(_Reason, _Timeout, #state{}) ->
    ok.

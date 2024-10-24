import pandas as pd

from bmll import reference
from bmll._utils import chunk_dates, to_pandas
from bmll._rest import DEFAULT_SESSION

__all__ = ('available', 'classified_trades', 'query', 'TimeSeriesClient')
DEFAULT_CHUNK_SIZE = 40_000


class TimeSeriesClient:
    """
    The TimeSeriesClient provides a convenient interface to interact with the BMLL Time-Series API.

    Args:

        session:
            `bmll.Session` (optional)

            if provided use this session object to communicate with the API, else use the default session.

        reference_client:
            `bmll.reference.ReferenceDataClient` (optional)

            if provided use this client to query the Reference Data API, else use `bmll.reference.query`.

    """

    def __init__(self, session=None, reference_client=None):
        self._session = session if session is not None else DEFAULT_SESSION
        self._reference_client = reference_client if reference_client is not None else reference

    def classified_trades(self,
                          *,
                          start_date,
                          end_date,
                          object_ids=None,
                          object_type='Listing',
                          chunk_size=100,
                          notional_currency='EUR',
                          finra_weekly=False,
                          combine_with_postdated_amendments=True,
                          **constraint):
        """
        Retrieve classified trades from the Time-Series Service.

        Args:

            constraint:
                Keyword arguments for constraints to search for reference data.

                For example:

                    MIC='XLON' or MIC=['XLON', 'XPAR']

                Allowed constraints include:
                    * MIC
                    * Ticker
                    * FIGI
                    * FIGIShareClass
                    * ISIN
                    * OPOL
                    * DisplayName
                    * Description.

                Note: constraints look for exact matches.

            start_date:
                as compatible with `pandas.to_datetime` (required)

                The start date (inclusive) for the query.

                See [pandas.to_datetime](

                    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html#pandas.to_datetime

                    ) for more information.

            end_date:
                as compatible with `pandas.to_datetime` (required)

                The end date (inclusive) for the query.

                See [pandas.to_datetime](

                    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html#pandas.to_datetime

                    ) for more information.

            object_ids:
                `list` of `int` (optional).

                The set of bmll ids for the query.

                This is required if no `constraints` are specified.

            object_type:
                `str` (optional)

                One of:
                    * Listing (default)
                    * Instrument
                    * Market

                Note: only used if a `constraint` is provided.

            chunk_size:
                `int` (optional), default 100

                Maximum number of object IDs to send in request.
                As there is a payload size limit, large requests must be broken down into multiple calls.
                SIP listings, in particular, tend to correspond to a larger payload as they span more trade categories.
                For more than one year of SIP data, a smaller chunk_size may therefore be required.

            notional_currency:
                `str (optional)

                The ISO currency code which notional amounts are converted to. This defaults to "EUR".

            finra_weekly:
                `Boolean (optional),  default `False`

                If True the query returns weekly aggregated classified trades with trades on Execution venue FINR
                breakdown if corresponding finra_weekly_summary data is available for given date range

            combine_with_postdated_amendments:
                `boolean (optional), default 'True'

                When true(default), classified trades daily aggregates are queried
                by `TradeDate` the values displayed contains any trade amendment reported later,
                `PublicationDate` will indicate the date of the latest amendment included.
                When false, classified trades daily reports are displayed as they were published on a
                specific `PublicationDate`, reports occurring for a different `TradeDate` will be displayed
                separately, values can be negative if the new report was mostly cancellations - users not
                interested in amendments can filter out the records where `PublicationDate` is different
                from `TradeDate` to obtain only the trade reports related to the `PublicationDate`.
        Examples:

            ```python
            classified_trades(start_date='2019-06-24',
                              end_date='2019-12-31',
                              object_ids=[121317])
            ```

        Returns:
            `pandas.DataFrame`:
                Time-Series Classified Trades DataFrame.

        """
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        object_column = object_type + 'Id'

        if constraint:
            object_ids, identifiers = self._get_market_grouped_ids_from_constraints(
                object_ids, object_type, object_column, constraint
            )
        else:
            # explicitly passed object ids are put into an all key
            # instead of being grouped by market
            object_ids = {'all': object_ids}

        request_kwargs = {
            'notional_currency': notional_currency,
            'finra_weekly': finra_weekly,
            'combine_with_postdated_amendments': combine_with_postdated_amendments
        }
        df = chunk_dates(
            object_ids, start_date, end_date, chunk_size, self._get_classified_trades_page, request_kwargs
        )
        if constraint:
            # pandas 0.23 raises when merging an object column with an int column
            identifiers = identifiers.astype({object_column: int})
            df = pd.merge(identifiers, df, left_on=[object_column], right_on=['ListingId'])

        return df

    def query(self,
              *,
              start_date,
              end_date,
              metric,
              frequency='D',
              object_ids=None,
              object_type='Listing',
              pivot=True,
              partial_results=False,
              chunk_size=DEFAULT_CHUNK_SIZE,
              **constraint):
        """
        Query the Time-Series Service.

        Args:

            constraint:
                Keyword arguments for constraints to search for reference data.

                For example:

                    MIC='XLON' or MIC=['XLON', 'XPAR']

                Allowed constraints include:
                    * MIC
                    * Ticker
                    * FIGI
                    * FIGIShareClass
                    * ISIN
                    * OPOL
                    * DisplayName
                    * Description.

                Note: constraints look for exact matches.

            start_date:
                as compatible with `pandas.to_datetime` (required)

                The start date (inclusive) for the query.

                See [pandas.to_datetime](
                    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html#pandas.to_datetime
                    ) for more information.

            end_date:
                as compatible with `pandas.to_datetime` (required)

                The end date (inclusive) for the query.

                See [pandas.to_datetime](
                    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html#pandas.to_datetime
                    ) for more information.

            metric:
                `str` or `list` of `str` or `dict` (required)

                The metric names as provided by `bmll.time_series.available`

                or

                A mongo query, see the [Mongo Documentation](
                https://docs.mongodb.com/manual/reference/method/db.collection.find/
                ) for more details.

            frequency:
                A frequency `str` as specified in `bmll.time_series.available` (optional)

                The default is 'D'

            object_ids:
                `list` of `int` (optional).

                The set of bmll ids for the query.

                This is required if no `constraints` are specified.

            object_type:
                `str` (optional)

                One of:
                    * Listing (default)
                    * Instrument
                    * Market

                Note: only used if a `constraint` is provided.

            pivot:
                `bool` (optional), default True.

                Whether to pivot the data so that each metric becomes a column.
                Otherwise, each metric is a row described by columns 'Metric' and 'Value'.

            partial_results:
                `bool` (optional), default False.

                If True, all permissioned data will be returned and any not permissioned
                will be omitted from the results.
                If False, the entire query will be rejected whenever any one of the requested
                objects is not permissioned.

            chunk_size:
                `int` (optional), default `DEFAULT_CHUNK_SIZE`

                Maximum number of object IDs to send in request.
                As there is a payload size limit, large requests must be broken down into multiple calls.

        Examples:

            ```python
            query(Ticker='VOD',
                  MIC='XLON',
                  metric='TradeCount',
                  frequency='D',
                  start_date='2019-06-24',
                  end_date='2019-12-31')
            ```

            ```python
            query(Ticker=['VOD', 'RDSA'],
                  MIC='XLON',
                  metric={
                      'metric': {'$in': ['TradeCount', 'TradeVolume']},
                      'tags.Classification':'LitAddressable'
                  },
                  frequency='D',
                  start_date='2019-06-24',
                  end_date='2019-12-31')
            ```

        Returns:
            `pandas.DataFrame`:
                Time-Series DataFrame.

        """
        if isinstance(metric, str):
            metric = [metric]
        elif isinstance(metric, pd.DataFrame):
            metric = _dataframe_to_query(metric)

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        object_column = object_type + 'Id'

        if constraint:
            object_ids, identifiers = self._get_market_grouped_ids_from_constraints(
                object_ids, object_type, object_column, constraint
            )
        else:
            # explicitly passed object ids are put into an all key
            # instead of being grouped by market
            object_ids = {'all': object_ids}

        request_kwargs = {
            'metrics': metric,
            'freq': frequency,
            'pivot': pivot,
            'partial_results': partial_results
        }
        df = chunk_dates(object_ids, start_date, end_date, chunk_size, self._get_query_page, request_kwargs)

        if constraint:
            df = pd.merge(identifiers, df, left_on=[object_column], right_on=['ObjectId'])
            del df['ObjectId']

        for ts_col in ['Timestamp', 'Date']:
            if ts_col in df:
                df[ts_col] = pd.to_datetime(df[ts_col])

        return df

    def available(self, object_id=None, explode_tags=False):
        """
        Return the metrics available.

        Args:

            object_id:
                `int` (optional)

                if provided, only return the metrics which exist for this object.

        Returns:

            `pandas.DataFrame`:
                The available metrics.

        """
        url = '/available'

        if object_id:
            url += f'/{object_id}'

        table = self._session.execute('get', 'time-series', url)
        df = to_pandas(table)

        if explode_tags:
            df = df.join(df.tags.apply(pd.Series))
            del df['tags']

        return df

    def _get_constrained_ref_data(
        self, object_ids, object_type, object_column, constraint, extra_cols=[]
    ):
        if object_ids:
            raise ValueError("Cannot provide 'object_ids' and 'constraint'")

        ref_data = self._reference_client.query(object_ids=object_ids,
                                                object_type=object_type,
                                                **constraint)
        if object_type == 'Instrument':
            # Only use reference data from the primary exchange for Instrument metrics.
            ref_data = ref_data.query('IsPrimary')

        ref_data_cols = list([object_column] + list(constraint))
        for col in extra_cols:
            if col not in ref_data_cols:
                ref_data_cols.append(col)
        identifiers = (
            ref_data[ref_data_cols]
            .drop_duplicates()  # no dupes
            .dropna(subset=[object_column])  # no Nans in ListingId/InstrumentId
        )
        return identifiers

    def _get_market_grouped_ids_from_constraints(
        self, object_ids, object_type, object_column, constraint
    ):
        """Find object_ids and identifiers for the given constraint using reference data."""
        identifiers = self._get_constrained_ref_data(
            object_ids, object_type, object_column, constraint, extra_cols=['MIC']
        )
        object_ids = identifiers.groupby('MIC')[object_column].apply(list).to_dict()

        if not object_ids:
            raise ValueError(f"No Object Ids found for given constraint. {constraint}")

        # drop mic from the indentifiers now we've used it
        if 'MIC' not in constraint:
            identifiers = identifiers.drop(columns=['MIC'])

        return object_ids, identifiers

    def _get_ids_from_constraints(self, object_ids, object_type, object_column, constraint):
        """Find object_ids and identifiers for the given constraint using reference data."""
        identifiers = self._get_constrained_ref_data(
            object_ids, object_type, object_column, constraint
        )
        object_ids = list(identifiers[object_column].unique())

        if not object_ids:
            raise ValueError(f"No Object Ids found for given constraint. {constraint}")

        return object_ids, identifiers

    def _get_query_page(self,
                        object_ids,
                        metrics,
                        freq,
                        start_date,
                        end_date,
                        pivot,
                        token=None,
                        partial_results=False):
        """ Helper function to form a request for a page for query().
        """
        payload = {
            'objectId': list({int(o) for o in object_ids}),
            'metric': metrics,
            'frequency': freq,
            'startDate': start_date.isoformat(),
            'endDate': end_date.isoformat(),
            'pivot': pivot,
            'partialResults': partial_results,
        }

        if token:
            payload['token'] = token
        return self._session.execute('post', 'time-series', '/query', json=payload)

    def _get_classified_trades_page(self, object_ids, start_date, end_date, notional_currency, finra_weekly=False,
                                    combine_with_postdated_amendments=True, token=None):
        payload = {
            'objectId': list({int(o) for o in object_ids}),
            'startDate': start_date.date().isoformat(),
            'endDate': end_date.date().isoformat(),
            'notionalCurrency': notional_currency,
            'combineWithPostdatedAmendments': combine_with_postdated_amendments
        }

        if finra_weekly:
            payload['finraWeekly'] = True

        if token:
            payload['token'] = token
        return self._session.execute('post', 'time-series', '/classified_trades', json=payload)


def _dataframe_to_query(df):
    assert 'metric' in df.columns
    assert 'suffix' in df.columns

    _or = df.loc[:, ['metric', 'suffix']].to_dict(orient='records')

    return {
        '$or': _or
    }


# we set up a default client and session so that users can still call
# bmll.time_series.query() etc.
_DEFAULT_CLIENT = TimeSeriesClient()
available = _DEFAULT_CLIENT.available
classified_trades = _DEFAULT_CLIENT.classified_trades
query = _DEFAULT_CLIENT.query

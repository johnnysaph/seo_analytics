from google_api_service import get_service
import pandas as pd
import logging
import sys


class GoogleSearchConsoleApi:
    """Class which incapsulates connection to Google Search Console API
    https://googleapis.github.io/google-api-python-client/docs/dyn/searchconsole_v1.html
    """

    def __init__(self):
        self._scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
        self._service = get_service("searchconsole", "v1", self._scopes)
        self.analytics = self._service.searchanalytics()

    def get_daily_report(self, site_url, dimensions, date, rowLimit=25000):
        body = {
            "aggregationType": "auto",
            "dimensions": dimensions,
            "startDate": date,
            "endDate": date,
            "rowLimit": rowLimit,
        }
        try:
            r = self.analytics.query(siteUrl=site_url, body=body).execute()
        except Exception as ex:
            logging.error("The following error occurred: {}".format(ex))
            sys.exit(1)
        else:
            if "rows" in r:  # got the data from sc
                df = pd.DataFrame.from_records(r["rows"])
                df["date"] = date
                df["website"] = site_url
                for i, dimension in enumerate(dimensions):
                    df[dimension] = df["keys"].apply(lambda x: x[i])
                df["position"] = df["position"].apply(lambda x: round(x, 2))
                # del df['keys']
                # del df['ctr']
                return df
            else:  # no data in sc for the current date
                logging.warning("Empty response from API")
                return pd.DataFrame()

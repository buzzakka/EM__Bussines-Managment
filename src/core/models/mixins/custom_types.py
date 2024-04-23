from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, Integer, text
from sqlalchemy.orm import mapped_column

sql_utc_now = text("TIMEZONE('utc', now())")

# Primary key
int_pk_T = Annotated[int, mapped_column(Integer, primary_key=True)]

# Datetime
created_at_T = Annotated[datetime, mapped_column(DateTime, server_default=sql_utc_now)]
updated_at_T = Annotated[datetime, mapped_column(
    DateTime,
    server_default=sql_utc_now,
    onupdate=sql_utc_now
)]
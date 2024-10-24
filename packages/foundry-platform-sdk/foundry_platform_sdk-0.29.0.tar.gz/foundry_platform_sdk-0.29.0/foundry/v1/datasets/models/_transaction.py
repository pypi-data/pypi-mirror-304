#  Copyright 2024 Palantir Technologies, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from __future__ import annotations

from datetime import datetime
from typing import Optional
from typing import cast

import pydantic

from foundry.v1.datasets.models._transaction_dict import TransactionDict
from foundry.v1.datasets.models._transaction_rid import TransactionRid
from foundry.v1.datasets.models._transaction_status import TransactionStatus
from foundry.v1.datasets.models._transaction_type import TransactionType


class Transaction(pydantic.BaseModel):
    """An operation that modifies the files within a dataset."""

    rid: TransactionRid

    transaction_type: TransactionType = pydantic.Field(alias="transactionType")

    status: TransactionStatus

    created_time: datetime = pydantic.Field(alias="createdTime")
    """The timestamp when the transaction was created, in ISO 8601 timestamp format."""

    closed_time: Optional[datetime] = pydantic.Field(alias="closedTime", default=None)
    """The timestamp when the transaction was closed, in ISO 8601 timestamp format."""

    model_config = {"extra": "allow"}

    def to_dict(self) -> TransactionDict:
        """Return the dictionary representation of the model using the field aliases."""
        return cast(TransactionDict, self.model_dump(by_alias=True, exclude_unset=True))

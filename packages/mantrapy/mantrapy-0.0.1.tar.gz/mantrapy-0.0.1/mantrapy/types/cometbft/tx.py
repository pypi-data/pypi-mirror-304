from dataclasses import dataclass


# TODO: add missing fields
@dataclass
class TxResult:
    code: int
    gas_wanted: str
    gas_used: str

    @classmethod
    def from_dict(cls, data: dict) -> 'TxResult':

        return cls(
            code=data['code'],
            gas_wanted=data['gas_wanted'],
            gas_used=data['gas_used'],
        )


@dataclass
class ResultTx:
    height: str
    tx_result: TxResult

    @classmethod
    def from_dict(cls, data: dict) -> 'ResultTx':

        tx_result = TxResult.from_dict(data['tx_result'])

        return cls(
            height=data['height'],
            tx_result=tx_result,
        )

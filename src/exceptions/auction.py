from fastapi import status


class AuctionError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Auction error"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.detail
        super().__init__(self.detail)


class LotNotFoundError(AuctionError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Lot not found"


class LotEndedError(AuctionError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Lot is already ended"


class BidTooLowError(AuctionError):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, current_price: str) -> None:
        super().__init__(
            f"Bid must be greater than current price {current_price}"
        )

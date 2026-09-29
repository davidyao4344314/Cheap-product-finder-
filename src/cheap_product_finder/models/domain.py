"""Core domain models; no retrieval or search behavior lives here."""

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Location:
    """A location that can start with only a city and grow more precise."""

    city: str | None = None
    region: str | None = None
    country: str | None = None
    postcode: str | None = None
    latitude: float | None = None
    longitude: float | None = None


@dataclass
class SearchRequest:
    """The user's original product query and requested location."""

    product_query: str
    location: Location


@dataclass
class ProductRequirement:
    """Structured product details, populated by a future parsing step."""

    original_query: str
    category: str | None = None
    brand: str | None = None
    model: str | None = None
    variant: str | None = None
    specifications: dict[str, str] = field(default_factory=dict)
    required_specifications: dict[str, str] = field(default_factory=dict)
    optional_specifications: dict[str, str] = field(default_factory=dict)


@dataclass
class Seller:
    """Identity and basic coverage details for a product source."""

    seller_id: str
    name: str
    website: str | None = None
    supported_regions: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class ProductListing:
    """A normalized offer, independent of how a seller supplied it."""

    seller: Seller
    title: str
    product_price: Decimal
    currency: str
    product_url: str
    brand: str | None = None
    model: str | None = None
    specifications: dict[str, str] = field(default_factory=dict)
    shipping_cost: Decimal = Decimal("0")
    fees: Decimal = Decimal("0")
    stock_status: str | None = None
    condition: str | None = None
    location: Location | None = None


@dataclass
class SearchResult:
    """Container for a future search workflow's listings and diagnostics."""

    request: SearchRequest
    location: Location
    valid_listings: list[ProductListing] = field(default_factory=list)
    rejected_listings: list[ProductListing] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    seller_statistics: dict[str, int] = field(default_factory=dict)

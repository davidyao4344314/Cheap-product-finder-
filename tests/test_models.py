"""Basic construction and default behavior for the domain objects."""

from decimal import Decimal
import unittest

from cheap_product_finder.models import (
    Location,
    ProductListing,
    ProductRequirement,
    SearchRequest,
    SearchResult,
    Seller,
)


class DomainModelTests(unittest.TestCase):
    def test_city_only_location_and_request(self) -> None:
        location = Location(city="Auckland")
        request = SearchRequest("Sony WH-1000XM6 Black", location)

        self.assertEqual(request.product_query, "Sony WH-1000XM6 Black")
        self.assertIs(request.location, location)
        self.assertIsNone(location.country)
        self.assertIsNone(location.latitude)

    def test_richer_location(self) -> None:
        location = Location(
            city="Auckland", region="Auckland", country="NZ",
            postcode="1010", latitude=-36.8485, longitude=174.7633,
        )
        self.assertEqual(location.postcode, "1010")
        self.assertEqual(location.longitude, 174.7633)

    def test_product_requirement_defaults_are_independent(self) -> None:
        first = ProductRequirement("Sony WH-1000XM6 Black")
        second = ProductRequirement("Sony WH-1000XM6 Silver")
        first.required_specifications["colour"] = "black"

        self.assertEqual(second.required_specifications, {})
        self.assertIsNone(first.model)
        self.assertEqual(first.optional_specifications, {})

    def test_seller_and_normalized_listing(self) -> None:
        seller = Seller("store-a", "Store A", "https://store.example", ("NZ",))
        listing = ProductListing(
            seller=seller,
            title="Sony WH-1000XM6 Black",
            product_price=Decimal("499.99"),
            currency="NZD",
            product_url="https://store.example/headphones",
            brand="Sony",
            model="WH-1000XM6",
            stock_status="in_stock",
            condition="new",
        )

        self.assertIs(listing.seller, seller)
        self.assertEqual(seller.supported_regions, ("NZ",))
        self.assertEqual(listing.shipping_cost, Decimal("0"))
        self.assertEqual(listing.fees, Decimal("0"))
        self.assertIsNone(listing.location)

    def test_result_containers_are_independent(self) -> None:
        request = SearchRequest("Sony WH-1000XM6", Location(city="Auckland"))
        first = SearchResult(request, request.location)
        second = SearchResult(request, request.location)
        first.errors.append("Seller unavailable")
        first.seller_statistics["store-a"] = 1

        self.assertEqual(second.errors, [])
        self.assertEqual(second.seller_statistics, {})
        self.assertEqual(first.valid_listings, [])
        self.assertEqual(first.rejected_listings, [])
        self.assertEqual(first.warnings, [])


if __name__ == "__main__":
    unittest.main()

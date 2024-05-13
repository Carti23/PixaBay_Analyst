import requests
import csv


class ImageFetcher:
    """Fetches images from the Pixabay API."""

    def __init__(
        self, api_key, image_type="photo", base_url="https://pixabay.com/api/"
    ):
        self.api_key = api_key
        self.image_type = image_type
        self.base_url = base_url

    def fetch_images(self, query, max_images):
        params = {
            "key": self.api_key,
            "q": query,
            "image_type": self.image_type,
            "per_page": 200,  # Max allowed by Pixabay
            "page": 1,
        }

        images = []
        total_hits = None
        while len(images) < max_images:
            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

                if "hits" not in data:
                    print(
                        "No 'hits' in response, likely an error with the API request."
                    )
                    break

                if total_hits is None:
                    total_hits = data["totalHits"]
                    print(f"Total available images for '{query}': {total_hits}")

                images.extend(data["hits"])
                print(
                    f"Fetched {len(data['hits'])} images on page {params['page']} for '{query}'. Total images so far: {len(images)}"
                )

                if len(images) >= total_hits or len(data["hits"]) < params["per_page"]:
                    print(f"No more images available to fetch for '{query}'.")
                    break

                params["page"] += 1
            except requests.RequestException as e:
                print(f"Request failed: {e}")
                break

        return images[:max_images]


class CSVWriter:
    """Handles CSV writing operations."""

    def __init__(self, filename, fieldnames):
        self.filename = filename
        self.fieldnames = fieldnames

    def write_to_csv(self, data):
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(
                    {field: item.get(field, "") for field in self.fieldnames}
                )


def main():
    # Your actual API key
    api_key = "43783254-71046eaff427f54e08a1e7770"
    fetcher = ImageFetcher(api_key)
    categories = {
        "yellow flowers": 4000,
        "nature": 4000,
        "lion": 4000,
        "laptop": 4000,
        "clothes": 4000,
        "cat": 4000,
        "money": 4000,
    }

    all_images = []
    for category, max_images in categories.items():
        fetched_images = fetcher.fetch_images(category, max_images)
        all_images.extend(fetched_images)

    fields = ["tags", "views", "downloads", "likes", "user", "comments"]
    csv_writer = CSVWriter("images.csv", fields)
    csv_writer.write_to_csv(all_images)


if __name__ == "__main__":
    main()

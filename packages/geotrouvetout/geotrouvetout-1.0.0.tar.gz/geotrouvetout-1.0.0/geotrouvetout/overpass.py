import overpy

def get_location_data(lat, lon, radius=1.0, max_age=365 * 24 * 60 * 60,
                      use_cache=True):
    query = f"""
    [out:json];
    node({lat - radius / 2},{lon - radius / 2},{lat + radius / 2},{lon + radius
/ 2});
    out center;
    """
      # node(around:5000,{lat},{lon})["name"]["addr:street"]["highway"];
      # way(around:5000,{lat},{lon})["name"]["addr:street"]["highway"];

    api = overpy.Overpass()
    result = api.query(query)

    print(len(result.nodes))
    print(len(result.ways))

    # location_data = {}
    # for elem in result.elements:
    #     if elem.tags.get("addr:street"):
    #         if "street_names" not in location_data:
    #             location_data["street_names"] = []
    #         location_data["street_names"].append(elem.tags["addr:street"])
    #     if elem.tags.get("name"):
    #         location_data["name"] = elem.tags["name"]
    #     if elem.tags.get("addr:city"):
    #         location_data["city"] = elem.tags["addr:city"]
    #     if elem.tags.get("addr:country"):
    #         location_data["country"] = elem.tags["addr:country"]
    #     if elem.tags.get("highway"):
    #         if "road_types" not in location_data:
    #             location_data["road_types"] = []
    #         location_data["road_types"].append(elem.tags["highway"])
    #
    # return location_data


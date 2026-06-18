def get_hotspots():

    hotspots = [
        {
            "id": 1,
            "location": "Metro Junction",
            "risk_score": 92,
            "latitude": 19.0760,
            "longitude": 72.8777
        },
        {
            "id": 2,
            "location": "Market Circle",
            "risk_score": 85,
            "latitude": 19.0820,
            "longitude": 72.8820
        }
    ]

    return {
        "success": True,
        "count": len(hotspots),
        "data": hotspots
    }
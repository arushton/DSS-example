from flask import Flask, render_template, jsonify
import s2sphere

app = Flask(__name__)

def generate_s2_cells(region_rect, level):
    coverer = s2sphere.RegionCoverer()
    coverer.min_level = level
    coverer.max_level = level
    coverer.max_cells = 500  # Adjust as needed

    cells = coverer.get_covering(region_rect)
    return [cell.id() for cell in cells]




@app.route('/')
def index():
    return render_template('s2CellsMapViewer.html')

@app.route('/get_s2_cells/<int:level>/<float(signed=True):sw_lat>/<float(signed=True):sw_lng>/<float(signed=True):ne_lat>/<float(signed=True):ne_lng>')
def get_s2_cells(level, sw_lat, sw_lng, ne_lat, ne_lng):
    print(level, sw_lat, sw_lng, ne_lat, ne_lng)
    # Create a lat-lng rectangle for the current viewable map area
    region_rect = s2sphere.LatLngRect.from_point_pair(
        s2sphere.LatLng.from_degrees(sw_lat, sw_lng),
        s2sphere.LatLng.from_degrees(ne_lat, ne_lng)
    )

    cell_ids = generate_s2_cells(region_rect, level)
    print("number of cell",len(cell_ids))
    cell_locations = []
    for cell_id in cell_ids:
        cell = s2sphere.CellId(cell_id)
        lat_lng = s2sphere.LatLng.from_point(s2sphere.Cell(cell).get_center())
        cell_locations.append({'lat': lat_lng.lat().degrees, 'lng': lat_lng.lng().degrees})
    return jsonify(cell_locations)


@app.route('/get_s2_cells_data/<int:level>/<float(signed=True):sw_lat>/<float(signed=True):sw_lng>/<float(signed=True):ne_lat>/<float(signed=True):ne_lng>')
def get_s2_cells_data(level, sw_lat, sw_lng, ne_lat, ne_lng):
    print(level, sw_lat, sw_lng, ne_lat, ne_lng)
    # Create a lat-lng rectangle for the current viewable map area
    region_rect = s2sphere.LatLngRect.from_point_pair(
        s2sphere.LatLng.from_degrees(sw_lat, sw_lng),
        s2sphere.LatLng.from_degrees(ne_lat, ne_lng)
    )

    cell_ids = generate_s2_cells(region_rect, level)
    print("Number of cells", len(cell_ids))
    cell_data = []

    for cell_id in cell_ids:
        cell = s2sphere.Cell(s2sphere.CellId(cell_id))
        vertices = []

        for i in range(4):  # Each cell is a quadrilateral
            vertex = cell.get_vertex(i)
            lat_lng = s2sphere.LatLng.from_point(vertex)
            vertices.append({'lat': lat_lng.lat().degrees, 'lng': lat_lng.lng().degrees})

        cell_data.append({'vertices': vertices})

    return jsonify(cell_data)

@app.route('/api/network-load')
def get_network_load():
    # Example data generation logic
    network_load_data = {f'Node-{i}': random.randint(0, 50) for i in range(1, 6)}

    return jsonify(network_load_data)



if __name__ == '__main__':
    app.run(debug=True)

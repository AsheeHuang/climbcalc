from flask import Flask, request, jsonify, render_template, send_from_directory
import heapq
import os
from collections import defaultdict, deque
from itertools import permutations

app = Flask(__name__)

class MountainGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.locations = set()
        
    def load_graph_data(self, file_path):
        """Load graph data from text file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    # Format: "start end time1 time2"
                    parts = line.split()
                    if len(parts) >= 3:
                        # Last two parts should be numbers (time1, time2)
                        try:
                            time2 = int(parts[-1])
                            time1 = int(parts[-2])
                            
                            # Everything before the numbers is location text
                            location_parts = parts[:-2]
                            
                            if len(location_parts) >= 2:
                                # Take first part as start, rest as end
                                start = location_parts[0]
                                end = ' '.join(location_parts[1:])
                                
                                self.locations.add(start)
                                self.locations.add(end)
                                
                                self.graph[start].append((end, time1))
                                self.graph[end].append((start, time2))
                        except ValueError:
                            # Skip lines where we can't parse numbers
                            continue
    
    def dijkstra(self, start, end):
        """Find shortest path using Dijkstra's algorithm"""
        if start not in self.locations or end not in self.locations:
            return None, float('inf'), []
        
        distances = {location: float('inf') for location in self.locations}
        distances[start] = 0
        previous = {}
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == end:
                path = []
                while current in previous:
                    path.append(current)
                    current = previous[current]
                path.append(start)
                path.reverse()
                
                # Calculate segment times
                segment_times = []
                for i in range(len(path) - 1):
                    current_loc = path[i]
                    next_loc = path[i + 1]
                    # Find the time between these two locations
                    for neighbor, weight in self.graph[current_loc]:
                        if neighbor == next_loc:
                            segment_times.append(weight)
                            break
                
                return path, distances[end], segment_times
            
            for neighbor, weight in self.graph[current]:
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        return None, float('inf'), []
    
    def calculate_multi_point_route(self, points):
        """Calculate shortest path through multiple points in order"""
        if len(points) < 2:
            return None, 0, []
        
        # Validate all points exist
        for point in points:
            if point not in self.locations:
                return None, float('inf'), []
        
        full_path = [points[0]]
        total_time = 0
        all_segment_times = []
        
        # Calculate path between each consecutive pair of points
        for i in range(len(points) - 1):
            start_point = points[i]
            end_point = points[i + 1]
            
            path, time, segment_times = self.dijkstra(start_point, end_point)
            
            if path is None:
                return None, float('inf'), []
            
            # Add path (excluding start point to avoid duplication)
            full_path.extend(path[1:])
            total_time += time
            all_segment_times.extend(segment_times)
        
        return full_path, total_time, all_segment_times


mountain_graph = MountainGraph()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/locations')
def get_locations():
    """Get all available locations"""
    return jsonify(sorted(list(mountain_graph.locations)))

@app.route('/api/calculate', methods=['POST'])
def calculate_climbing_time():
    """Calculate shortest climbing time through multiple points"""
    data = request.get_json()
    
    # Support both old format (start/end) and new format (points list)
    if 'points' in data:
        points = data.get('points')
        if not points or len(points) < 2:
            return jsonify({'error': 'At least 2 points are required'}), 400

    path, time, segment_times = mountain_graph.calculate_multi_point_route(points)
    
    if path is None:
        return jsonify({'error': 'No path found between the locations'}), 404
    
    return jsonify({
        'path': path,
        'points': points,
        'time': time,
        'time_formatted': f"{time // 60}h {time % 60}m" if time < float('inf') else "No path",
        'segment_times': segment_times,
        'segment_times_formatted': [f"{t}m" for t in segment_times]
    })

@app.route('/api/load_graph/<graph_name>')
def load_graph(graph_name):
    """Load a specific graph file"""
    file_path = f"graphs/{graph_name}.txt"
    if os.path.exists(file_path):
        mountain_graph.graph.clear()
        mountain_graph.locations.clear()
        mountain_graph.load_graph_data(file_path)
        return jsonify({'message': f'Graph {graph_name} loaded successfully', 'locations': len(mountain_graph.locations)})
    else:
        return jsonify({'error': 'Graph file not found'}), 404

@app.route('/images/<filename>')
def serve_image(filename):
    """Serve images from the images directory"""
    return send_from_directory('images', filename)


if __name__ == '__main__':
    mountain_graph.load_graph_data('graphs/G02.txt')
    app.run(debug=True)
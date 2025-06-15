from flask import Flask, request, jsonify, render_template
import heapq
import os
from collections import defaultdict, deque

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
            return None, float('inf')
        
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
                return path, distances[end]
            
            for neighbor, weight in self.graph[current]:
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        return None, float('inf')

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
    """Calculate shortest climbing time between two locations"""
    data = request.get_json()
    start = data.get('start')
    end = data.get('end')
    
    if not start or not end:
        return jsonify({'error': 'Start and end locations are required'}), 400
    
    path, time = mountain_graph.dijkstra(start, end)
    
    if path is None:
        return jsonify({'error': 'No path found between the locations'}), 404
    
    return jsonify({
        'path': path,
        'time': time,
        'time_formatted': f"{time // 60}h {time % 60}m" if time < float('inf') else "No path"
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

if __name__ == '__main__':
    mountain_graph.load_graph_data('graphs/G02.txt')
    app.run(debug=True)
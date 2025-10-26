#!/usr/bin/env python3
"""
Vastu Blueprint Generator - Professional Floor Plans
Generates detailed, realistic floor plan blueprints with NO blank spaces
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc
import numpy as np
import io
import base64

app = Flask(__name__)
CORS(app)

def draw_door(ax, x, y, width, height, direction='right'):
    """Draw a door with arc"""
    if direction == 'right':
        door_arc = Arc((x, y + height/2), width*0.6, height*0.6, 
                      angle=0, theta1=0, theta2=90, color='black', linewidth=2)
        ax.add_patch(door_arc)
        ax.plot([x, x + width*0.3], [y + height/2, y + height/2], 'k-', linewidth=2)
    elif direction == 'top':
        door_arc = Arc((x + width/2, y), width*0.6, height*0.6,
                      angle=0, theta1=180, theta2=270, color='black', linewidth=2)
        ax.add_patch(door_arc)
        ax.plot([x + width/2, x + width/2], [y, y + height*0.3], 'k-', linewidth=2)

def draw_furniture(ax, room_type, x, y, width, height):
    """Draw furniture based on room type"""
    cx, cy = x + width/2, y + height/2
    
    if 'bedroom' in room_type.lower():
        # Bed
        bed_w, bed_h = min(width*0.5, 6), min(height*0.6, 8)
        bed = patches.Rectangle((cx - bed_w/2, cy - bed_h/2), bed_w, bed_h,
                                linewidth=2, edgecolor='#333', facecolor='#D3D3D3')
        ax.add_patch(bed)
        # Pillow
        pillow = patches.Rectangle((cx - bed_w/2, cy + bed_h/2 - 1), bed_w, 1,
                                   linewidth=1, edgecolor='#333', facecolor='white')
        ax.add_patch(pillow)
        
    elif 'living' in room_type.lower() or 'drawing' in room_type.lower():
        # Sofa
        sofa_w, sofa_h = min(width*0.6, 8), min(height*0.3, 4)
        sofa = patches.Rectangle((cx - sofa_w/2, y + height*0.25), sofa_w, sofa_h,
                                 linewidth=2, edgecolor='#333', facecolor='#A9A9A9')
        ax.add_patch(sofa)
        # Table
        table = plt.Circle((cx, cy - height*0.15), min(width, height)*0.15,
                          color='#8B4513', alpha=0.4, linewidth=2, edgecolor='#333')
        ax.add_patch(table)
        
    elif 'kitchen' in room_type.lower():
        # Counter
        counter_w, counter_h = width*0.85, height*0.25
        counter = patches.Rectangle((x + width*0.075, y + height*0.1), counter_w, counter_h,
                                    linewidth=2, edgecolor='#333', facecolor='#C0C0C0')
        ax.add_patch(counter)
        # Stove circles
        for i in range(2):
            stove = plt.Circle((x + width*0.3 + i*width*0.35, y + height*0.225), 0.5,
                              color='black', alpha=0.6)
            ax.add_patch(stove)
        # Sink
        sink = patches.Rectangle((x + width*0.75, y + height*0.15), width*0.18, height*0.15,
                                 linewidth=2, edgecolor='#333', facecolor='#87CEEB')
        ax.add_patch(sink)
        
    elif 'bathroom' in room_type.lower():
        # Toilet
        toilet = plt.Circle((x + width*0.25, y + height*0.7), min(width, height)*0.12,
                           color='white', linewidth=2, edgecolor='#333')
        ax.add_patch(toilet)
        # Sink
        sink = plt.Circle((x + width*0.75, y + height*0.75), min(width, height)*0.12,
                         color='#87CEEB', linewidth=2, edgecolor='#333')
        ax.add_patch(sink)
        # Bathtub
        bathtub = patches.Rectangle((x + width*0.5, y + height*0.15), width*0.45, height*0.35,
                                    linewidth=2, edgecolor='#333', facecolor='#B0E0E6', alpha=0.5)
        ax.add_patch(bathtub)
        
    elif 'dining' in room_type.lower():
        # Table
        table_w, table_h = min(width*0.6, 6), min(height*0.5, 6)
        table = patches.Rectangle((cx - table_w/2, cy - table_h/2), table_w, table_h,
                                  linewidth=2, edgecolor='#333', facecolor='#8B4513', alpha=0.4)
        ax.add_patch(table)
        # Chairs
        for pos in [(cx - table_w/2 - 0.7, cy), (cx + table_w/2 + 0.7, cy),
                    (cx, cy - table_h/2 - 0.7), (cx, cy + table_h/2 + 0.7)]:
            chair = plt.Circle(pos, 0.5, color='#696969', linewidth=1, edgecolor='#333')
            ax.add_patch(chair)

def generate_complete_blueprint(rooms, plot_width, plot_height, layout_type='optimal'):
    """Generate a complete blueprint with NO blank spaces"""
    
    fig, ax = plt.subplots(figsize=(16, 16))
    fig.patch.set_facecolor('#F5F5F5')
    ax.set_facecolor('#FFFFFF')
    
    margin = 3
    ax.set_xlim(-margin, plot_width + margin)
    ax.set_ylim(-margin, plot_height + margin)
    ax.set_aspect('equal')
    
    # Outer walls (thick)
    outer_wall = patches.Rectangle((0, 0), plot_width, plot_height,
                                   linewidth=8, edgecolor='#000', facecolor='none')
    ax.add_patch(outer_wall)
    
    # Generate complete room layouts (NO BLANK SPACES)
    room_layouts = []
    num_rooms = len(rooms) if rooms else 4
    
    if layout_type == 'optimal':
        # OPTIMAL VASTU LAYOUT - Complete coverage
        room_layouts = [
            # Row 1 (Top) - 3 sections
            {'name': 'Bathroom', 'x': plot_width*0.7, 'y': plot_height*0.67, 
             'width': plot_width*0.3, 'height': plot_height*0.33, 'type': 'bathroom'},
            {'name': 'Bedroom-2', 'x': plot_width*0.35, 'y': plot_height*0.67, 
             'width': plot_width*0.35, 'height': plot_height*0.33, 'type': 'bedroom'},
            {'name': 'Pooja/Store', 'x': 0, 'y': plot_height*0.67, 
             'width': plot_width*0.35, 'height': plot_height*0.33, 'type': 'pooja room'},
            
            # Row 2 (Middle) - 3 sections
            {'name': 'Living Room', 'x': 0, 'y': plot_height*0.33, 
             'width': plot_width*0.5, 'height': plot_height*0.34, 'type': 'living room'},
            {'name': 'Dining', 'x': plot_width*0.5, 'y': plot_height*0.33, 
             'width': plot_width*0.25, 'height': plot_height*0.34, 'type': 'dining room'},
            {'name': 'Passage', 'x': plot_width*0.75, 'y': plot_height*0.33, 
             'width': plot_width*0.25, 'height': plot_height*0.34, 'type': 'passage'},
            
            # Row 3 (Bottom) - 3 sections
            {'name': 'Master Bedroom', 'x': 0, 'y': 0, 
             'width': plot_width*0.4, 'height': plot_height*0.33, 'type': 'bedroom'},
            {'name': 'Bathroom-2', 'x': plot_width*0.4, 'y': 0, 
             'width': plot_width*0.25, 'height': plot_height*0.33, 'type': 'bathroom'},
            {'name': 'Kitchen', 'x': plot_width*0.65, 'y': 0, 
             'width': plot_width*0.35, 'height': plot_height*0.33, 'type': 'kitchen'},
        ]
        
    elif layout_type == 'modern':
        # MODERN LAYOUT - Complete coverage
        room_layouts = [
            # Top row
            {'name': 'Bedroom-1', 'x': 0, 'y': plot_height*0.6, 
             'width': plot_width*0.5, 'height': plot_height*0.4, 'type': 'bedroom'},
            {'name': 'Bedroom-2', 'x': plot_width*0.5, 'y': plot_height*0.6, 
             'width': plot_width*0.5, 'height': plot_height*0.4, 'type': 'bedroom'},
            
            # Middle row
            {'name': 'Living+Dining', 'x': 0, 'y': plot_height*0.3, 
             'width': plot_width*0.6, 'height': plot_height*0.3, 'type': 'living room'},
            {'name': 'Kitchen', 'x': plot_width*0.6, 'y': plot_height*0.3, 
             'width': plot_width*0.4, 'height': plot_height*0.3, 'type': 'kitchen'},
            
            # Bottom row
            {'name': 'Bathroom-1', 'x': 0, 'y': 0, 
             'width': plot_width*0.3, 'height': plot_height*0.3, 'type': 'bathroom'},
            {'name': 'Bathroom-2', 'x': plot_width*0.3, 'y': 0, 
             'width': plot_width*0.3, 'height': plot_height*0.3, 'type': 'bathroom'},
            {'name': 'Store/Utility', 'x': plot_width*0.6, 'y': 0, 
             'width': plot_width*0.4, 'height': plot_height*0.3, 'type': 'store room'},
        ]
        
    else:  # compact
        # COMPACT LAYOUT - Complete grid coverage
        room_layouts = [
            # Top row
            {'name': 'Bedroom-1', 'x': 0, 'y': plot_height*0.67, 
             'width': plot_width*0.5, 'height': plot_height*0.33, 'type': 'bedroom'},
            {'name': 'Bedroom-2', 'x': plot_width*0.5, 'y': plot_height*0.67, 
             'width': plot_width*0.5, 'height': plot_height*0.33, 'type': 'bedroom'},
            
            # Middle row
            {'name': 'Living Room', 'x': 0, 'y': plot_height*0.33, 
             'width': plot_width*0.5, 'height': plot_height*0.34, 'type': 'living room'},
            {'name': 'Dining', 'x': plot_width*0.5, 'y': plot_height*0.33, 
             'width': plot_width*0.5, 'height': plot_height*0.34, 'type': 'dining room'},
            
            # Bottom row
            {'name': 'Kitchen', 'x': 0, 'y': 0, 
             'width': plot_width*0.5, 'height': plot_height*0.33, 'type': 'kitchen'},
            {'name': 'Bathroom', 'x': plot_width*0.5, 'y': 0, 
             'width': plot_width*0.5, 'height': plot_height*0.33, 'type': 'bathroom'},
        ]
    
    # Draw all rooms
    for room_data in room_layouts:
        x, y = room_data['x'], room_data['y']
        width, height = room_data['width'], room_data['height']
        room_name = room_data['name']
        room_type = room_data['type']
        
        # Interior walls
        if x > 0:
            ax.plot([x, x], [y, y + height], 'k-', linewidth=4)
        if y > 0:
            ax.plot([x, x + width], [y, y], 'k-', linewidth=4)
        
        # Room label
        cx, cy = x + width/2, y + height/2
        ax.text(cx, cy + height*0.35, room_name.upper(), 
               ha='center', va='center', fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='white', 
                        edgecolor='#666', alpha=0.9, linewidth=2))
        
        # Dimensions
        dim_text = f"{int(width)}' × {int(height)}'"
        ax.text(cx, cy - height*0.35, dim_text,
               ha='center', va='center', fontsize=9, style='italic', 
               color='#555', fontweight='600')
        
        # Furniture
        draw_furniture(ax, room_type, x, y, width, height)
        
        # Doors
        if 'bathroom' not in room_type.lower() and 'passage' not in room_type.lower():
            if x > 0 and width > 4:
                draw_door(ax, x, y + height*0.45, width*0.1, height*0.15, 'right')
    
    # Compass
    compass_x = plot_width + margin*0.6
    compass_y = plot_height + margin*0.6
    compass_size = 2.5
    
    # North arrow (red)
    ax.arrow(compass_x, compass_y, 0, compass_size, 
            head_width=0.7, head_length=0.7, fc='red', ec='red', linewidth=2)
    ax.text(compass_x, compass_y + compass_size + 0.8, 'N', 
           ha='center', fontsize=14, fontweight='bold', color='red')
    
    # Other directions
    ax.text(compass_x + compass_size*0.8, compass_y, 'E', 
           ha='center', fontsize=11, fontweight='bold', color='#333')
    ax.text(compass_x, compass_y - compass_size*0.8, 'S', 
           ha='center', fontsize=11, fontweight='bold', color='#333')
    ax.text(compass_x - compass_size*0.8, compass_y, 'W', 
           ha='center', fontsize=11, fontweight='bold', color='#333')
    
    # Title
    title_map = {
        'optimal': 'OPTIMAL VASTU LAYOUT',
        'modern': 'MODERN FUNCTIONAL LAYOUT',
        'compact': 'COMPACT EFFICIENT LAYOUT'
    }
    ax.text(plot_width/2, plot_height + margin*0.8, title_map.get(layout_type, 'FLOOR PLAN'),
           ha='center', fontsize=18, fontweight='bold', color='#2A363B',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='#F4A261', alpha=0.8))
    
    # Scale
    scale_length = 10
    scale_y = -margin*0.6
    ax.plot([5, 5 + scale_length], [scale_y, scale_y], 'k-', linewidth=3)
    ax.plot([5, 5], [scale_y - 0.4, scale_y + 0.4], 'k-', linewidth=3)
    ax.plot([5 + scale_length, 5 + scale_length], [scale_y - 0.4, scale_y + 0.4], 'k-', linewidth=3)
    ax.text(5 + scale_length/2, scale_y - 1.2, f"SCALE: {scale_length} FEET",
           ha='center', fontsize=10, fontweight='bold', style='italic')
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    
    # Save
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=200, bbox_inches='tight', facecolor='#F5F5F5')
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route('/generate_blueprints', methods=['POST', 'OPTIONS'])
def generate_blueprints():
    """Generate professional blueprints"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        print("🏗️ Received blueprint generation request")
        
        plot_size = data.get('plotSize', '1200 sq ft')
        rooms = data.get('rooms', [])
        orientation = data.get('orientation', 'north-facing')
        
        plot_area = 1200
        try:
            plot_area = int(''.join(filter(str.isdigit, plot_size)))
        except:
            pass
        
        plot_width = int(plot_area ** 0.5)
        plot_height = plot_area // plot_width
        
        print(f"📐 Plot: {plot_width}x{plot_height}, Rooms: {len(rooms)}")
        
        blueprints = []
        layouts = [
            {'type': 'optimal', 'name': 'Optimal Vastu Layout', 'score': 95, 
             'desc': 'Perfect Vastu compliance with ideal room placements'},
            {'type': 'modern', 'name': 'Modern Functional Layout', 'score': 80,
             'desc': 'Contemporary design with Vastu principles'},
            {'type': 'compact', 'name': 'Compact Efficient Layout', 'score': 72,
             'desc': 'Space-efficient with maximum utilization'}
        ]
        
        for i, layout in enumerate(layouts):
            print(f"🎨 Generating blueprint {i+1}/3 ({layout['name']})...")
            img = generate_complete_blueprint(rooms, plot_width, plot_height, layout['type'])
            
            blueprints.append({
                'id': i + 1,
                'name': layout['name'],
                'description': layout['desc'],
                'vastu_score': layout['score'],
                'image': img
            })
        
        print(f"✅ Generated {len(blueprints)} professional blueprints!")
        
        return jsonify({
            'success': True,
            'blueprints': blueprints,
            'plot_info': {
                'width': plot_width,
                'height': plot_height,
                'area': plot_area,
                'orientation': orientation
            }
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': str(e),
            'blueprints': []
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'professional_blueprint_generator'})

if __name__ == '__main__':
    print("=" * 70)
    print("🏗️ VASTU VISION - PROFESSIONAL BLUEPRINT GENERATOR")
    print("=" * 70)
    print("✅ NO BLANK SPACES - Complete room allocation")
    print("✅ Professional furniture and fixtures")
    print("✅ Detailed dimensions and labels")
    print("🌐 Server: http://localhost:5002")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5002, debug=True)

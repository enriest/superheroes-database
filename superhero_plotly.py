
import plotly.graph_objects as go
import pandas as pd

# Option 1: Using mysql-connector-python
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    print("MySQL packages not installed. Install with:")
    print("pip install mysql-connector-python")
    MYSQL_AVAILABLE = False

if MYSQL_AVAILABLE:
    # MySQL connection configuration with better error handling
    mysql_config = {
        'host': 'localhost',  # Replace with your MySQL server
        'user': 'root',  # Replace with your username
        'password': 'huwsev-Jetwed-wykwe9',  # Replace with your password
        'database': 'superhero',  # Your database name
        'auth_plugin': 'mysql_native_password'  # Try this if having auth issues
    }
    
    try:
        # Create connection with error handling
        conn = mysql.connector.connect(**mysql_config)
        print("✅ Successfully connected to MySQL!")
    except mysql.connector.Error as err:
        print(f"❌ MySQL Connection Error: {err}")
        print("Common solutions:")
        print("1. Check if MySQL server is running")
        print("2. Verify username and password")
        print("3. Check if database 'superhero' exists")
        print("4. Try connecting without specifying database first")
        MYSQL_AVAILABLE = False

# Diagnostic code - run this first to test basic connection
def test_mysql_connection():
    """Test MySQL connection with different configurations"""
    
    # Test 1: Basic connection without database
    try:
        test_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'huwsev-Jetwed-wykwe9'
        }
        test_conn = mysql.connector.connect(**test_config)
        print("✅ Basic MySQL connection successful!")
        
        # Show available databases
        cursor = test_conn.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
        print("📋 Available databases:")
        for db in databases:
            print(f"   - {db[0]}")
        
        test_conn.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ Basic connection failed: {err}")
        return False

if MYSQL_AVAILABLE:
    try:
        # Get both Intelligence and Strength data
        intelligence_query = """
        SELECT 
            s.superhero_name,
            ha.attribute_value,
            p.publisher_name,
            'Intelligence' as attribute_type
        FROM superhero s
        LEFT JOIN 
            hero_attribute ha ON s.id = ha.hero_id
        LEFT JOIN 
            attribute a ON ha.attribute_id = a.id
        LEFT JOIN
            publisher p ON s.publisher_id = p.id
        WHERE ha.attribute_id = 1 AND ha.attribute_value = 100 AND (s.publisher_id = 4 OR s.publisher_id = 13)
        ORDER BY ha.attribute_value DESC;
        """
        
        strength_query = """
        SELECT 
            s.superhero_name,
            ha.attribute_value,
            p.publisher_name,
            'Strength' as attribute_type
        FROM superhero s
        LEFT JOIN 
            hero_attribute ha ON s.id = ha.hero_id
        LEFT JOIN 
            attribute a ON ha.attribute_id = a.id
        LEFT JOIN
            publisher p ON s.publisher_id = p.id
        WHERE ha.attribute_id = 2 AND ha.attribute_value = 100 AND (s.publisher_id = 4 OR s.publisher_id = 13)
        ORDER BY ha.attribute_value DESC;
        """
        
        # Execute both queries
        df_intelligence = pd.read_sql_query(intelligence_query, conn)
        df_strength = pd.read_sql_query(strength_query, conn)
        conn.close()  # Close the connection after use
        
        print(f"✅ Intelligence query: Found {len(df_intelligence)} records.")
        print(f"✅ Strength query: Found {len(df_strength)} records.")
        
        # Adding color mapping for Marvel (red) and DC (blue)
        def get_color(publisher):
            publisher_str = str(publisher).lower()
            if 'marvel' in publisher_str:
                return 'Marvel'
            elif 'dc' in publisher_str:
                return 'DC Comics'
            else:
                return 'Unknown'
        
        
        # Apply color mapping to both datasets
        df_intelligence['publisher_category'] = df_intelligence['publisher_name'].apply(get_color)
        df_strength['publisher_category'] = df_strength['publisher_name'].apply(get_color)
        
    except Exception as e:
        print(f"❌ Query execution error: {e}")
        df_intelligence = None
        df_strength = None

else:
    print("Cannot execute query - MySQL packages not available")
    df_intelligence = None
    df_strength = None

# Create Interactive Plotly table with dropdown selector
if df_intelligence is not None and df_strength is not None:
    print(f"✅ Creating interactive table with dropdown selector")
    
    # Helper function for row colors
    def get_row_color(publisher_category):
        if publisher_category == 'Marvel':
            return '#FFE6E6'  # Light red background
        elif publisher_category == 'DC Comics':
            return '#E6E6FF'  # Light blue background
        else:
            return '#F0F0F0'  # Light gray background (fallback)
    
    # Prepare data for Intelligence table
    intel_data = df_intelligence[['superhero_name', 'publisher_name', 'publisher_category']].copy()
    intel_colors = [get_row_color(cat) for cat in intel_data['publisher_category']]
    
    # Prepare data for Strength table  
    strength_data = df_strength[['superhero_name', 'publisher_name', 'publisher_category']].copy()
    strength_colors = [get_row_color(cat) for cat in strength_data['publisher_category']]
    
    # Create the interactive figure with dropdown
    fig = go.Figure()
    
    # Add Intelligence table (visible by default)
    fig.add_trace(go.Table(
        header=dict(
            values=['<b>Superhero Name</b>', '<b>Publisher</b>'],
            fill_color='#40466e',
            font=dict(color='white', size=14),
            align="center",
            height=40
        ),
        cells=dict(
            values=[intel_data['superhero_name'], intel_data['publisher_name']],
            fill_color=[intel_colors, intel_colors],
            font=dict(color='black', size=12),
            align="left",
            height=35
        ),
        visible=True,
        name="Intelligence"
    ))
    
    # Add Strength table (hidden by default)
    fig.add_trace(go.Table(
        header=dict(
            values=['<b>Superhero Name</b>', '<b>Publisher</b>'],
            fill_color='#40466e',
            font=dict(color='white', size=14),
            align="center",
            height=40
        ),
        cells=dict(
            values=[strength_data['superhero_name'], strength_data['publisher_name']],
            fill_color=[strength_colors, strength_colors],
            font=dict(color='black', size=12),
            align="left",
            height=35
        ),
        visible=False,
        name="Strength"
    ))
    
    # Add dropdown menu
    fig.update_layout(
        title="Superheroes with Maximum Attributes",
        height=800,
        margin=dict(l=20, r=20, t=100, b=20),
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=[{"visible": [True, False]}],
                        label="Intelligence",
                        method="restyle"
                    ),
                    dict(
                        args=[{"visible": [False, True]}],
                        label="Strength", 
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.02,
                yanchor="top"
            ),
        ]
    )
    
    fig.show()

else:
    print("No data available to plot")

# Justice League vs Avengers Strength Comparison
if MYSQL_AVAILABLE:
    try:
        # Reconnect to database for the team comparison queries
        conn = mysql.connector.connect(**mysql_config)
        
        # Justice League query
        justice_league_query = """
        SELECT 
            s.superhero_name,
            ha.attribute_value as strength,
            (
                SELECT sum(ha2.attribute_value)
                FROM superhero s2
                LEFT JOIN hero_attribute ha2 ON s2.id = ha2.hero_id AND ha2.attribute_id = 2
                WHERE s2.superhero_name IN ('Batman', 'Superman', 'Wonder Woman', 'Aquaman', 'Flash', 'Green Lantern', 'Martian Manhunter')
            ) as total_group_strength
        FROM superhero s
        LEFT JOIN hero_attribute ha ON s.id = ha.hero_id AND ha.attribute_id = 2
        WHERE s.superhero_name IN ('Batman', 'Superman', 'Wonder Woman', 'Aquaman', 'Flash', 'Green Lantern', 'Martian Manhunter')
        GROUP BY s.superhero_name, ha.attribute_value
        ORDER BY s.superhero_name DESC;
        """
        
        # Avengers query  
        avengers_query = """
        SELECT 
            s.superhero_name,
            ha.attribute_value as strength,
            (
                SELECT sum(ha2.attribute_value)
                FROM superhero s2
                LEFT JOIN hero_attribute ha2 ON s2.id = ha2.hero_id AND ha2.attribute_id = 2
                WHERE s2.superhero_name IN ('Hulk', 'Iron Man', 'Thor', 'Captain America', 'Hawkeye', 'Black Widow', 'Ant-Man')
            ) as total_group_strength
        FROM superhero s
        LEFT JOIN hero_attribute ha ON s.id = ha.hero_id AND ha.attribute_id = 2
        WHERE s.superhero_name IN ('Hulk', 'Iron Man', 'Thor', 'Captain America', 'Hawkeye', 'Black Widow', 'Ant-Man')
        GROUP BY s.superhero_name, ha.attribute_value
        ORDER BY s.superhero_name DESC;
        """
        
        # Execute queries
        df_justice_league = pd.read_sql_query(justice_league_query, conn)
        df_avengers = pd.read_sql_query(avengers_query, conn)
        conn.close()
        
        print(f"✅ Justice League query: Found {len(df_justice_league)} members.")
        print(f"✅ Avengers query: Found {len(df_avengers)} members.")
        
        # Create the comparison chart
        if not df_justice_league.empty and not df_avengers.empty:
            # X-axis will be hero names and team labels
            jl_names = df_justice_league['superhero_name'].tolist()
            av_names = df_avengers['superhero_name'].tolist()
            
            # Y-axis will be individual strength values
            jl_strengths = df_justice_league['strength'].fillna(0).tolist()
            av_strengths = df_avengers['strength'].fillna(0).tolist()
            
            fig = go.Figure()
            
            # Add Justice League bar
            fig.add_bar(
                x=[["Justice League"] * len(jl_names), jl_names],
                y=jl_strengths,
                name="Justice League",
                marker_color='#0000FF',
                text=[f"{name}: {strength}" for name, strength in zip(jl_names, jl_strengths)],
                textposition='auto'
            )
            
            # Add Avengers bar (trace 1) 
            fig.add_bar(
                x=[["Avengers"] * len(av_names), av_names],
                y=av_strengths,
                name="Avengers", 
                marker_color='#FF0000',
                text=[f"{name}: {strength}" for name, strength in zip(av_names, av_strengths)],
                textposition='auto'
            )
            
            # Update layout
            fig.update_layout(
                title="Justice League vs Avengers - Individual Strength Comparison",
                xaxis_title="Teams and Heroes",
                yaxis_title="Strength Value",
                barmode="group",  # Changed from "relative" to "group" for better comparison
                height=600,
                showlegend=True,
                font=dict(size=12)
            )
            
            # Show total team strengths in subtitle
            jl_total = df_justice_league['total_group_strength'].iloc[0] if not df_justice_league.empty else 0
            av_total = df_avengers['total_group_strength'].iloc[0] if not df_avengers.empty else 0
            
            fig.update_layout(
                title=f"Justice League vs Avengers - Individual Strength Comparison<br><sub>Total Team Strength: Justice League ({jl_total}) vs Avengers ({av_total})</sub>"
            )
            
            fig.show()
            
            print(f"📊 Justice League total strength: {jl_total}")
            print(f"📊 Avengers total strength: {av_total}")
            print(f"🏆 Stronger team: {'Justice League' if jl_total > av_total else 'Avengers' if av_total > jl_total else 'Tie'}")
            
        else:
            print("❌ No team data found")
            
    except Exception as e:
        print(f"❌ Team comparison query error: {e}")
        
else:
    print("Cannot execute team comparison - MySQL packages not available")
import altair as alt
import streamsync as ss
import pandas as pd
import seaborn as sns
import matplotlib.colors as mcolors

# INIT

data = pd.DataFrame({'a': list('CCCDDDEEE'),
                     'b': [10, 7, 4, 1, 2, 6, 8, 4, 1]})
chart = alt.Chart(data).mark_bar().encode(
    x='a',
    y='average(b)'
).configure_mark(color='#fdc5fd')

data_cereal = pd.read_csv("demoData/cereal.csv")

print("Hello world! You'll see this message in the log")

hacker_pigeons_df = pd.DataFrame({
    "name": ["Byte", "Scoop", "Pixel", "Cache", "Bandwidth", "Algo", "Firewall", "Gizmo", "Query", "Iris"],
    "role": ["leader", "data analyst", "developer", "developer", "developer", "developer", "security expert", "hardware engineer", "data analyst", "UI/UX designer"],
    "feather_color": ["dark", "grey", "white", "brown", "black", "blue", "red", "green", "purple", "pink"],
    "eye_color": ["sparkling", "brown", "blue", "green", "amber", "grey", "hazel", "yellow", "black", "rainbow"],
    "specialty": ["bridging gap between species", "investigative reporting", "data visualization", "data storage optimization", "networking and communication", "algorithm design", "system protection", "device integration", "database management", "user experience optimization"]
})

role_counts = hacker_pigeons_df['role'].value_counts().reset_index()
role_counts.columns = ['role', 'count']

hardcoded_palette = [
    '#fdc5fd',
    '#f27df9',
    '#ed58f7',
    '#e934f5',
    '#e50ff3',
    '#e10cf1'
]

# Create a new DataFrame column 'color' to store the color palette
role_counts['color'] = hardcoded_palette

# Create an Altair bar chart with the hardcoded color palette
pigeon_chart = alt.Chart(role_counts).mark_bar().encode(
    x=alt.X('role', title='Role'),
    y=alt.Y('count', title='Number of Pigeons'),
    color=alt.Color('color', scale=None, legend=None)
).properties(
    title='Number of Hacker Pigeons by Role',
    width=400,
    height=400
)

role_feather_counts = (
    hacker_pigeons_df.groupby(["role", "feather_color"])
    .size()
    .reset_index(name="count")
)

# Create a faceted Altair bar chart
second_pigeon_chart = (
    alt.Chart(role_feather_counts)
    .mark_bar()
    .encode(
        x=alt.X("role", title="Role"),
        y=alt.Y("count", title="Number of Pigeons"),
        color=alt.Color("feather_color", legend=alt.Legend(title="Feather Color")),
        tooltip=["role", "feather_color", "count"],
    )
    .properties(title="Number of Hacker Pigeons by Role and Feather Color")
    .facet(facet=alt.Facet("feather_color", title="Feather Color"), columns=4)
    .resolve_scale(x="independent")
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)


# STATE INIT

ss.init_state({
    "counter": 10,
    "chart": chart,
    "pigeon_chart": pigeon_chart,
    "second_pigeon_chart": second_pigeon_chart,
    "data_cereal": data_cereal,
    "hacker_pigeons_df": hacker_pigeons_df,
    "my_bytes": ss.pack_bytes(b'\x31\x33\x33\x37', mime_type="text/plain")
})

# EVENT HANDLERS

def increment(state):

    """
    Increments counter by one.
    """

    state["counter"] += 1


def slow_handler():

    """
    Example of a non-blocking, slow operation.
    """

    print("Slow handler triggered. You'll see this message in the log.")
    import time
    time.sleep(2)


def failing_handler():
    a = 1/0
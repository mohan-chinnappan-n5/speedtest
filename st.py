import streamlit as st
from speedtest import Speedtest  # Make sure:  pip install speedtest-cli is installed correctly
# speedtest-cli==2.1.3 in requirements.txt

# Function to run the speed test and retrieve detailed information
def measure_speed():
    st.write("Retrieving speedtest configuration...")
    tester = Speedtest()
    tester.get_best_server()

    # Get additional server information
    server = tester.get_best_server()
    isp_info = {
        "ISP": tester.config['client']['isp'],
        "IP Address": tester.config['client']['ip'],
        "Server Location": f"{server['sponsor']} ({server['name']}, {server['country']})",
        "Distance": f"{server['d']:.2f} km",
        "Ping": f"{server['latency']:.2f} ms"
    }

    # Measure download and upload speeds
    download_speed = tester.download() / 1_000_000  # Convert to Mbps
    upload_speed = tester.upload() / 1_000_000      # Convert to Mbps

    return isp_info, download_speed, upload_speed

# Streamlit layout
st.title("Network Speed Test Dashboard")

# Button to start the speed test
if st.button("Run Speed Test"):
    with st.spinner("Running speed test..."):
        isp_info, download_speed, upload_speed = measure_speed()

    # Sidebar for Connection Details
    with st.sidebar:
        st.header("Connection Details")
        st.write(f"**ISP**: {isp_info['ISP']}")
        st.write(f"**IP Address**: {isp_info['IP Address']}")
        st.write(f"**Server Location**: {isp_info['Server Location']}")
        st.write(f"**Distance**: {isp_info['Distance']}")
        st.write(f"**Ping**: {isp_info['Ping']}")

    # Display download and upload speeds in main area
    st.subheader("Speed Test Results")
    st.write(f"**Download Speed**: {download_speed:.2f} Mbps")
    st.write(f"**Upload Speed**: {upload_speed:.2f} Mbps")

    # Plotting donut chart with Plotly
    import plotly.graph_objects as go
    fig = go.Figure(data=[go.Pie(
        labels=["Download Speed", "Upload Speed"],
        values=[download_speed, upload_speed],
        hole=.4,
        marker=dict(colors=["#4CAF50", "#FF7043"])
    )])

    fig.update_layout(
        title_text="Network Speed Test Results",
        annotations=[dict(text="Mbps", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    st.plotly_chart(fig)
else:
    st.write("Click 'Run Speed Test' to measure your network speed.")
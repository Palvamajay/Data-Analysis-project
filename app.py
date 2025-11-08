# importing the needed libraries 
import pandas as pd
import matplotlib.pyplot as plt
import time
import streamlit as st
import warnings as wt
wt.filterwarnings('ignore')

# creating the title for the app 
title=st.title("Data Analysis App")


uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])



if uploaded_file is not None:
    # File is uploaded
    if uploaded_file.name.endswith(".csv"):
        st.success("✅ Yes, this is a CSV file and it’s uploaded successfully!")

        df=pd.read_csv(uploaded_file)
        

        st.subheader("🔍 Data Preview")
        st.write(df.head())
    else:
        st.warning("⚠️ The uploaded file is not a CSV file.")
else:
    st.info("📂 Please upload a CSV file to continue.")


st.markdown("---")


# checking for the columns 
st.subheader('General Information')
des=st.selectbox("select the info you need",["columns","shape","tail","missing_valuse","data_types"])

if des=="columns":
    st.write(df.columns)
elif des=="shape":
    st.write(df.shape)
elif des=="tail":
    st.write(df.tail()) 
elif des=='missing_valuse':
    st.write(df.isnull().sum().sum())
elif des=="data_types":
    st.write(df.dtypes)               
st.markdown("---")
# creating the different analysis 

categories = st.selectbox(
    "Select a category:",
    ["Correleation", "Describe", "Duplicates"]
)
# numerical columns 
num_df = df.select_dtypes(include=['number'])

# creating the analysis 
if categories == "Correleation":
    st.write("You selected Correleation 🧮")
    st.write(num_df.corr())
elif categories == "Describe":
    st.write("You selected Describe")
    st.write(df.describe())
elif categories == "Duplicates":
    st.write("You selected Duplicates ")
    if df.duplicated().sum() >= 1:
       st.write(f"There are {df.duplicated().sum()} duplicate rows in the dataset.")
    else:
      st.write("There are no duplicate rows in the dataset.")
 
# data cleaning 
st.markdown('---')
st.subheader("Clean the data")

st.subheader("🧹 Data Cleaning Options")

data_clean = st.selectbox("Select the cleaning operation:", 
                          ['Remove Duplicates', 'Remove Null Values'])

if st.button("Click here"):
    if data_clean == "Remove Duplicates":
        st.write("🔄 Removing duplicates...")
        with st.spinner("Processing..."):
            df.drop_duplicates(inplace=True)
            time.sleep(2)
        st.success("✅ Duplicates removed successfully!")
        st.dataframe(df)

    elif data_clean == "Remove Null Values":
        st.write("🧽 Removing null values...")
        with st.spinner("Processing..."):
            df.dropna(inplace=True)
            time.sleep(2)
        st.success("✅ Null values removed successfully!")
        st.dataframe(df)

st.markdown("---")

# Sidebar for selecting columns




# --- Plot selection ---
plot = st.selectbox("Select the plot:", ["Line_plot", "Bar_chart", "Area_chart"])

# --- Line Plot ---
if plot == "Line_plot":
    st.subheader("You selected Line Chart 📈")
    x_axis = st.selectbox("Select X-axis:", num_df.columns)
    y_axis = st.selectbox("Select Y-axis:", num_df.columns)
    st.line_chart(num_df[[x_axis, y_axis]])
    
# --- Bar Chart ---
elif plot == "Bar_chart":
    st.subheader("You selected Bar Chart 📊")
    x_axis1 = st.selectbox("Select X-axis (categorical):", df.select_dtypes(include=["object", "category"]).columns.tolist())
    y_axis1 = st.selectbox("Select Y-axis (numerical):", df.select_dtypes(include=["number"]).columns)
    st.bar_chart(df.set_index(x_axis1)[y_axis1])

# --- Area Chart ---
elif plot == "Area_chart":
    st.subheader("You selected Area Chart 🌈")
    x_axis = st.selectbox("Select X-axis:", num_df.columns)
    y_axis = st.selectbox("Select Y-axis:", num_df.columns)
    st.area_chart(num_df[[x_axis, y_axis]])
st.markdown('---')
# --- Additional Plot Options ---
title2=st.subheader("🧠More Analysis")

plots2 = st.radio("Pick a plot type:", ("Scatter_plot", "Correlation_plot"))

# --- Scatter Plot ---
if plots2 == "Scatter_plot":
    st.title("Scatter Plot using Matplotlib 🎨")
    x_axis_scar = st.selectbox("Select X-axis:", num_df.columns, key="scatter_x")
    y_axis_scar = st.selectbox("Select Y-axis:", num_df.columns, key="scatter_y")
    
    fig, ax = plt.subplots()
    ax.scatter(df[x_axis_scar], df[y_axis_scar], color='blue', s=100, alpha=0.7)
    ax.set_xlabel(x_axis_scar)
    ax.set_ylabel(y_axis_scar)
    ax.set_title(f"{x_axis_scar} vs {y_axis_scar}")
    st.pyplot(fig)

# --- Correlation Plot ---
elif plots2 == "Correlation_plot":
    st.title("Correlation Plot 🔗")
    fig, ax = plt.subplots()
    corr_matrix = num_df.corr()
    cax = ax.matshow(corr_matrix, cmap='coolwarm')
    fig.colorbar(cax)
    
    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_yticks(range(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, rotation=90)
    ax.set_yticklabels(corr_matrix.columns)
    ax.set_title("Correlation Matrix", pad=20)
    
    st.pyplot(fig)
st.markdown("---")    

st.subheader("📥 Download Cleaned File")

# --- Convert DataFrame to CSV ---
csv_data = df.to_csv(index=False).encode('utf-8')

# --- Download Button ---
st.download_button(
    label="Click here to download the file 📂",
    data=csv_data,
    file_name="cleaned_data.csv",
    mime="text/csv"
)



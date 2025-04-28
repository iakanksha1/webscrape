import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
    scrape_with_subpages
)
from parse import parse_with_ollama

# Streamlit UI
st.title("AI Web Scraper")
url = st.text_input("Enter Website URL")

# Configuration for subpage scraping
with st.expander("Advanced Scraping Options"):
    include_subpages = st.checkbox("Include subpages", value=False)
    max_depth = st.slider("Maximum depth level", 1, 5, 1, 
                         help="How many links deep to follow from the main page")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")
        
        if include_subpages:
            # Use the new subpage scraper
            with st.spinner(f"Scraping {url} and its subpages (this may take a while)..."):
                # Create a placeholder for real-time updates
                status_container = st.empty()
                
                # Start the scraping process
                results = scrape_with_subpages(url, max_depth=max_depth)
                
                # Store the combined content in session state
                combined_content = "\n\n---\n\n".join([
                    f"URL: {page_url}\n\n{content}" 
                    for page_url, content in results.items()
                ])
                st.session_state.dom_content = combined_content
                st.session_state.page_results = results
                
                # Display summary
                st.success(f"Successfully scraped {len(results)} pages")
                
                # Display the results
                for i, (page_url, content) in enumerate(results.items()):
                    with st.expander(f"Page {i+1}: {page_url}"):
                        st.text_area(f"Content from {page_url}", content, height=200)
        else:
            # Original single-page scraping
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the DOM content in Streamlit session state
            st.session_state.dom_content = cleaned_content

            # Display the DOM content in an expandable text box
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)

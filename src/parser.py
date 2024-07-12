from bs4 import BeautifulSoup

def parse_search_results(html_content, query, start_position):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []

    for item in soup.find_all('li', {'class': 'b_algo'}):
        title = item.find('h2').text if item.find('h2') else "No title"
        link = item.find('a')['href'] if item.find('a') else "No link"
        description = item.find('p').text if item.find('p') else "No description"
        
        result = {
            "Title": title,
            "link": link,
            "Description": description,
            "Position": start_position + len(results) + 1
        }
        results.append(result)

    return results

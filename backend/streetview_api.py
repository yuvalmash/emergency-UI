# import google_streetview as gsv

# Define parameters for street view api
# params = [{
#     'size': '600x300', # max 640x640 pixels
#     'location': '32.053016, 34.772589',
#     'heading': '0;90;180;270',
#     # 'pitch': '-0.76',
#     'key': 'AIzaSyBgPmnoaTooWJdgcHor2jUeCMFRv40ekkA'
# }]
#
# # Create a results object
# results = gsv.api.results(params)
#
# # Download images to directory 'downloads'
# results.download_links('streetview')


import google_streetview.api
import google_streetview.helpers

# Create a dictionary with multiple parameters separated by ;
apiargs = {
  'location': '32.053016, 34.772589',
  'size': '640x640',
  'heading': '0;90;180;270',
  'key': 'AIzaSyBgPmnoaTooWJdgcHor2jUeCMFRv40ekkA'
}

# Get a list of all possible queries from multiple parameters
api_list = google_streetview.helpers.api_list(apiargs)

# Create a results object for all possible queries
results = google_streetview.api.results(api_list)

# Download images to directory 'downloads'
results.download_links('streetview')

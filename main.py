import requests
import pandas as pd
import os
import urllib.request
import glob
from Montage import Montage
import cv2


# convert the search result into dataframe
def getDataFrame(search_results):
    # the fields in the results that will be stored
    column_names = ['Names', 'Price', 'Prime', 'ImageURL']
    # create a dataframe
    df = pd.DataFrame(columns=column_names)
    for result in search_results:
        # store the name
        name = result['title']
        try:
            # try to store the price if given
            price = result['price']['value']
        except:
            # else, set the price to be -1
            price = -1
        try:
            # try to store the prime
            prime = result['is_prime']
        except:
            # else, set the prime to be False
            prime = False
        # store the image url
        imageURL = result['image']
        # append the row to the dataframe
        df.loc[len(df.index)] = name, price, prime, imageURL
    # filter out the rows where the prime is False
    df = df[df['Prime'] == True]
    # sort the values acording to the price in a descending order
    df = df.sort_values(by=['Price'], ascending=False)
    # reset the index of the rows
    df.reset_index(drop=False, inplace=True)
    return df


# save the images given the dataframe and the folder path
def saveImages(dataFrame, folder):
    # save the images using url into the folder
    for idx, row in dataFrame.iterrows():
        url = row['ImageURL']
        urllib.request.urlretrieve(url, folder + '/' + str(idx) + '.jpg')
    print('images are saved in folder ' + folder)


# save the images as montage given the folder of the images
def saveImagesAsMont(folder):
    # retrieve the file path and names for the images
    files = []
    for file in sorted(glob.glob(folder + '/*.jpg')):
        files.append(file)
    # read the first file as the initial image for the montage
    initial_image = cv2.imread(files[0])
    mont = Montage(initial_image)
    # append the images to montage
    for file in files[1:]:
        image = cv2.imread(file)
        mont.append(image)
    # save the montage1D
    mont.save("./" + folder + "/montage.jpg")
    # save the montage2D
    mont.saveMontage2D("./" + folder + "/montage2D.jpg")



if __name__ == '__main__':

    # search_term = "memory cards"
    search_term = input("Enter a text input to search\n")

    # set up the request parameters
    params = {
        'api_key': '1C2234C904164A218CC0C11BC3F31582',
        'type': 'search',
        'amazon_domain': 'amazon.co.uk',
        'search_term': search_term,
        'page': '10',
        'output': 'json'
    }
    # make the http GET request to Rainforest API
    api_result = requests.get('https://api.rainforestapi.com/request', params)
    # get the dataframe using the search result
    df = getDataFrame(api_result.json()['search_results'])
    # save the dataframe as csv file
    df.to_csv(search_term + '.csv', index=True)
    # create the image folder for the search result
    image_folder = search_term + " images"
    try:
        os.mkdir(image_folder)
    except:
        print("Failed to create the folder. The folder might already exist.")
    # save the images into the folder
    saveImages(df, "./" + image_folder)
    # save the images as montage
    saveImagesAsMont("./" + image_folder)


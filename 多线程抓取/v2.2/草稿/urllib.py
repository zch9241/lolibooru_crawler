import urllib.request

url = 'https://lolibooru.moe/image/cd92aa1084e46e72e2f11853ec5c8243/lolibooru%20354429%20faceless_male%20hair_ornament%20head_out_of_frame%20height_difference%20looking_away%20photoshop_(medium)%20spoken_ellipsis%20translation_request%20upper_body.jpg'

def download(a,b,c):
     load = a*b*100/c
     print(load)


urllib.request.urlretrieve(url,reporthook = download)
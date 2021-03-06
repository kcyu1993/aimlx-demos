from flask import Blueprint
from flask import Flask, abort
from flask import jsonify
from flask import render_template
from flask import request, send_from_directory
import jsonpickle
import json
import requests
import config as conf
import helpers
import os
from . import chestxray


@chestxray.route('', methods=['GET'])
def ask_for_image():
    return render_template('chestxray.html')


@chestxray.route('/upload', methods=['POST'])
def upload():
    global processed_images
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(APP_ROOT, conf.chestxray['dir'])

    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("directory already present: {}".format(target))

    print('Upload')
    f = request.files
    destination = ''
    for upload in request.files.getlist("fileToUpload"):
        print(type(upload))
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # destination = "/".join([target, "temp.jpg"])
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        # print(upload.read())
        upload.save(destination)

    test_url = conf.chestxray['url']

    # prepare headers for http request
    content_type = 'application/json'
    headers = {'content-type': content_type}

    list = {'image_list': destination}

    # send http request with image and receive response
    response = requests.post(test_url, data=jsonpickle.encode(list), headers=headers)
    # decode response
    print(json.loads(response.text))

    im_name = os.path.basename(destination)
    im_name_out0 = im_name.split('.')[0] + '_out0.jpg'
    im_name_out1 = im_name.split('.')[0] + '_out1.jpg'
    im_name_out2 = im_name.split('.')[0] + '_out2.jpg'
    im_name_out3 = im_name.split('.')[0] + '_out3.jpg'
    processed_images = [im_name_out3, im_name_out0, im_name_out1, im_name_out2]
    # return render_template("grocery_gallery.html", image_names=processed_images)
    return json.dumps({'list': processed_images})


@chestxray.route('/static', methods=['POST'])
def for_static():
    global processed_images
    r = request
    data = r.data

    destination = jsonpickle.decode(data.decode('utf-8'))['image_list']

    data = {'image_list': os.path.join(conf.chestxray['dir'], destination)}

    test_url = conf.chestxray['url']

    # prepare headers for http request
    content_type = 'application/json'
    headers = {'content-type': content_type}

    # send http request with image and receive response
    response = requests.post(test_url, data=jsonpickle.encode(data), headers=headers)
    if response is not None:
        # decode response
        print("for static decode response ", json.loads(response.text))

    im_name = os.path.basename(destination)
    im_name_out0 = im_name.split('.')[0] + '_out0.jpg'
    im_name_out1 = im_name.split('.')[0] + '_out1.jpg'
    im_name_out2 = im_name.split('.')[0] + '_out2.jpg'
    im_name_out3 = im_name.split('.')[0] + '_out3.jpg'
    processed_images = [im_name_out3, im_name_out0, im_name_out1, im_name_out2]
    # return render_template("grocery_gallery.html", image_names=processed_images)
    return json.dumps({'list': processed_images})





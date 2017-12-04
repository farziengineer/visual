# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from vis_mod.models import Document
from vis_mod.forms import DocumentForm

from PIL import Image
import random
import sys
from visual.settings import BASE_DIR
import os


def utils(fil):
    image = Image.open(fil)
    image = image.convert('1')

    outfile1 = Image.new("1", [dimension * 2 for dimension in image.size])

    outfile2 = Image.new("1", [dimension * 2 for dimension in image.size])

    for x in range(0, image.size[0], 2):
        for y in range(0, image.size[1], 2):
            sourcepixel = image.getpixel((x, y))
            assert sourcepixel in (0, 255)
            coinflip = random.random()
            if sourcepixel == 0:
                if coinflip < .5:
                    outfile1.putpixel((x * 2, y * 2), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2), 0)
                    outfile1.putpixel((x * 2, y * 2 + 1), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 255)
                    
                    outfile2.putpixel((x * 2, y * 2), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2), 255)
                    outfile2.putpixel((x * 2, y * 2 + 1), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 0)
                else:
                    outfile1.putpixel((x * 2, y * 2), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2), 255)
                    outfile1.putpixel((x * 2, y * 2 + 1), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)
                    
                    outfile2.putpixel((x * 2, y * 2), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2), 0)
                    outfile2.putpixel((x * 2, y * 2 + 1), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255)
            elif sourcepixel == 255:
                if coinflip < .5:
                    outfile1.putpixel((x * 2, y * 2), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2), 0)
                    outfile1.putpixel((x * 2, y * 2 + 1), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 255)
                    
                    outfile2.putpixel((x * 2, y * 2), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2), 0)
                    outfile2.putpixel((x * 2, y * 2 + 1), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255)
                else:
                    outfile1.putpixel((x * 2, y * 2), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2), 255)
                    outfile1.putpixel((x * 2, y * 2 + 1), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)
                    
                    outfile2.putpixel((x * 2, y * 2), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2), 255)
                    outfile2.putpixel((x * 2, y * 2 + 1), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 0)
    print "Bad"+BASE_DIR
    # print "asd"+os.path.join(BASE_DIR, '/media/images/out1.jpg')
    outfile1.save(BASE_DIR+'/media/images/out1.jpg')
    outfile2.save(BASE_DIR+ '/media/images/out2.jpg')
    link1 = "/media/images/out1.jpg"
    link2 = "/media/images/out2.jpg"
    return [link1, link2]


def util2(f1, f2):
    from PIL import Image
    import sys
    import numpy as np


    infile1 = Image.open(f1)
    infile2 = Image.open(f2)
    imgs = [infile1, infile2 ]

    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

    imgs_comb = Image.fromarray( imgs_comb)


    outfile1 = Image.new('1', infile1.size)
    outfile2 = Image.new('1', infile1.size)
    for x in range(infile1.size[0]):
        for y in range(infile1.size[1]):
            outfile2.putpixel((x, y), (infile1.getpixel((x, y)) ^ infile2.getpixel((x, y))))
            outfile1.putpixel((x, y), (infile1.getpixel((x, y)) or infile2.getpixel((x, y))))

    outfile2.save(BASE_DIR+'/media/images/xor.jpg')
    outfile1.save(BASE_DIR+'/media/images/or.jpg')

    link1 = "/media/images/xor.jpg"
    link2 = "/media/images/or.jpg"
    return [link1, link2]




def list(request):
    # Handle file upload
    curr_image=1
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            lis=utils(request.FILES['docfile'])
            newdoc.save()
            lis.append(newdoc.docfile.url)
            lis.extend(util2(BASE_DIR+"/media/images/out1.jpg", 
                BASE_DIR+"/media/images/out2.jpg"))
            # Redirect to the document list after POST
            return render(request, 'list.html',{'form': form, 'lis':lis} )
    else:
        form = DocumentForm()  # A empty, unbound form

    # print curr_image.docfile.url
    return render(
        request,
        'list.html',
        {'form': form }
    )
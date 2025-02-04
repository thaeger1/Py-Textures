import numpy as np
import tkinter as tk
import b64encoder as encoder


class ImageFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, width=256, height=256, relief=tk.RIDGE, bd=4)
        self.grid_propagate(False)

        self.activeImages = []

        self.img = tk.PhotoImage()
        self.imgLabel = tk.Label(self, image=self.img)

        self.imgLabel.grid(column=0,row=0)
        self.grid(column=0,row=0)

        # TODO: add background grid

    def updateImage(self):
        # new blank img
        imgOut = np.empty((256,256,4), dtype=np.uint)
        # sum layers
        numImg = len(self.activeImages)
        for i in range(numImg):
            imgOut += self.activeImages[i]
        # normalize
        imgOut = (imgOut//numImg).astype(np.uint8)
        # convert to b64
        istr = encoder.arr_to_b64(imgOut)
        # update img
        self.img = tk.PhotoImage(data=istr)
        # update imgLabel
        self.imgLabel.configure(image=self.img)
        self.imgLabel.image = self.img

    def clearImage(self):
        self.img = tk.PhotoImage()
        self.imgLabel.configure(image=self.img)
        self.imgLabel.image = self.img

class ImageLayer(tk.Frame):
    def __init__(self, root, idx):
        # super().__init__(root)
        tk.Frame.__init__(self, root, width=100, height=32, padx=4, pady=4)

        # self.idx = idx

        # img data
        data = np.empty((256,256,4), dtype=np.uint8)
        for i in range(256*256):
            x, y = i % 256, i//256
            data[y,x] = [0, 255-y, x, 255] # uv coords

        self.imgData = data
        b64 = encoder.arr_to_b64(data)
        tImage = tk.PhotoImage(data=b64, width=256, height=256)

        self.cstate = tk.IntVar()
        self.checkbox = tk.Checkbutton(self, onvalue=idx, variable=self.cstate, command= lambda: root.toggleVis(self.cstate.get(), self.imgData))

        self.subimg = tImage.subsample(8)
        self.subframe = tk.Label(self, image=self.subimg, width=32, height=32) # 256 / 32

        self.checkbox.grid(column=0,row=0)
        self.subframe.grid(column=1,row=0)
        self.grid(column=0,row=idx, padx=4, pady=4)

        # TODO: add operator drop down
        # TODO: add background grid

class LayerFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, width=88, height=256, relief=tk.RIDGE, bd=4) # vframe
        self.root = root
        self.grid_propagate(False)

        self.arrLayers = []
        for i in range(1,root.numLayers+1):
            self.arrLayers.append(ImageLayer(self, i))

        self.grid(column=1,row=0)

    ### TODO: call showImage from root
    # check checkbox state
    def toggleVis(self, idx, data):
        if (idx > 0):
            self.root.addActiveImage(data)
        else:
            self.root.removeActiveImage(data)

class Toolbar(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, width=344, height=64, relief=tk.RIDGE, bd=4)
        self.grid_propagate(False)

        self.xoff, self.yoff = tk.IntVar(), tk.IntVar()

        def mycallback(var, idx, mode):
            # if blank, return
            # print(self.tools.getvar(var))
            # print(self.tools.getint(var))
            print(self.xoff.get())
            print(self.yoff.get())

            # root.UpdateImageData()

        # self.tools.xoff.trace_add('write', mycallback)
        # self.tools.yoff.trace_add('write', mycallback)

        xoffLab, yoffLab = tk.Label(self, text='x off'), tk.Label(self, text="y off")
        self.xoffEnt, self.yoffEnt = tk.Entry(self, width=4, textvariable=self.xoff), tk.Entry(self, width=4, textvariable=self.yoff)

        # xscaleLab, yscaleLab = tk.Label(self, text='x scale'), tk.Label(self, text="y scale")
        # xscale, yscale = tk.Entry(self, width=4), tk.Entry(self, width=4)

        # open button
        # save button

        # active layer entry

        xoffLab.grid(column=0,row=0)
        yoffLab.grid(column=0,row=1)
        self.xoffEnt.grid(column=1,row=0)
        self.yoffEnt.grid(column=1,row=1)

        # xscaleLab.grid(column=2,row=0)
        # yscaleLab.grid(column=2,row=1)
        # xscale.grid(column=3,row=0)
        # yscale.grid(column=3,row=1)

        self.grid(column=0,row=1,columnspan=2)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tkinter PhotoImage Demo')
        self.geometry('348x324') # 8px buf

        self.numLayers = 1
        self.activeImage = 0

        self.iframe = ImageFrame(self)
        self.layers = LayerFrame(self)
        self.tools = Toolbar(self)

    def updateImageData(self, params):
        # params = (xoff, yoff, xscale, yscale)
        # tell layerframe to calc new imgdata based on params
        return

    def addActiveImage(self, newImg):
        self.iframe.activeImages.append(newImg)
        self.iframe.updateImage()
        # print(len(self.iframe.activeImages))

    def removeActiveImage(self, imgToRemove):
        self.iframe.activeImages.remove(imgToRemove)
        if (len(self.iframe.activeImages) == 0): self.iframe.clearImage()
        # del self.iframe.activeImages[self.iframe.activeImages.index(imgToRemove)]

if __name__ == "__main__":
    app = App()
    app.mainloop()

from PIL import Image


def joinImagesInFolder(folderToStoreProcessedImage: str, index, score, imagesFolderName: str):
    images = [Image.open(x) for x in [f'{imagesFolderName}/{index}_0_{score}.png', f'{imagesFolderName}/{index}_90_{score}.png', f'{imagesFolderName}/{index}_180_{score}.png', f'{imagesFolderName}/{index}_270_{score}.png']]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save(f'{folderToStoreProcessedImage}/{index}_joined_{score}.png')
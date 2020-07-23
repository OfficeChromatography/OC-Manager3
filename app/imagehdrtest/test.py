import cv2 as cv
import numpy as np

def test_mertens(images, exposure_times):

    # Convert to grey scale
    grey_images = []
    for i in images:
        grey_images.append(cv.cvtColor(i,cv.COLOR_BGR2GRAY))

    # Find size of 1 of the images
    sz = grey_images[0].shape

    # Define the motion model
    warp_mode = cv.MOTION_TRANSLATION

    # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if warp_mode == cv.MOTION_HOMOGRAPHY :
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else :
        warp_matrix = np.eye(2, 3, dtype=np.float32)

    # Number of iterations
    number_of_iterations = 5000;

    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-10;
    criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
    # inputMask = cv.noArray()
	# Run the ECC algorithm. The results are stored in warp_matrix.
    aligned_images = []
    for i in range(1,len(images)):
        (cc, warp_matrix) = cv.findTransformECC(grey_images[0],grey_images[i],warp_matrix, warp_mode, criteria, grey_images[i], 5)

        if warp_mode == cv.MOTION_HOMOGRAPHY :
            aligned_images.append(cv.warpPerspective (images[i], warp_matrix, (sz[1],sz[0]), flags=cv.INTER_LINEAR + cv.WARP_INVERSE_MAP))
        else:
            aligned_images.append(cv.warpAffine(images[i], warp_matrix, (sz[1],sz[0]), flags=cv.INTER_LINEAR + cv.WARP_INVERSE_MAP))

        cv.imwrite(f'./results/aligned_image/aligned_image{i}.jpeg', aligned_images[i-1])
        cv.imwrite(f'./results/aligned_image/aligned_image0.jpeg', images[0])


    img_fn = ["aligned_image0.jpeg", "aligned_image1.jpeg", "aligned_image2.jpeg", "aligned_image3.jpeg"]
    img_list = [cv.imread('./results/aligned_image/'+fn) for fn in img_fn]

    # Exposure fusion using Mertens
    merge_mertens = cv.createMergeMertens()
    res_mertens = merge_mertens.process(img_list)
    res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
    cv.imwrite("./results/aligned_image/fusion_mertens_aligned.jpeg", res_mertens_8bit)




img_fn = ["img0.jpeg", "img1.jpeg", "img2.jpeg", "img3.jpeg"]
img_list = [cv.imread(fn) for fn in img_fn]
exposure_times = np.array([0.0333, 0.25, 2.5, 15.0], dtype=np.float32)
[15.0, 2.5, 0.25, 0.0333]
# # Merge exposures to HDR image
#
# merge_debevec = cv.createMergeDebevec()
# hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy())
#
# merge_robertson = cv.createMergeRobertson()
# hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())

test_mertens(img_list,exposure_times)


# # Tonemap HDR image
# tonemap1 = cv.createTonemap(gamma=1.2)
# res_debevec = tonemap1.process(hdr_debevec.copy())
# res_robertson = tonemap1.process(hdr_robertson.copy())

# tonemap = cv.createTonemapMantiuk(gamma = 1.2, scale = 1, saturation = 5.0)
# res_debevec = tonemap.process(hdr_debevec.copy())
# res_robertson = tonemap.process(hdr_robertson.copy())
#
# # Convert datatype to 8-bit and save
# res_debevec_8bit = np.clip(res_debevec*255, 0, 255).astype('uint8')
# res_robertson_8bit = np.clip(res_robertson*255, 0, 255).astype('uint8')
# res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
# #
# cv.imwrite("./results/ldr_debevec.jpg", res_debevec_8bit)
# cv.imwrite("./results/ldr_robertson.jpg", res_robertson_8bit)

<h1 align="center">
  <span style="color:#00FFFF;"> ٠ ࣪⭑CubeSat Star Tracker๋࣭ ⭑</span>
</h1>



## ✦ Summary ✦

This project presents a MATLAB-based prototype of a star tracker pipeline developed to explore the fundamentals of spacecraft attitude determination using star field images. The system operates on BMP images captured from an MT9P031 CMOS sensor and demonstrates key steps involved in real-world star tracker algorithms.

The imaging process is approximated using a pinhole camera model to convert 2D pixel coordinates into 3D unit vectors. Lens distortion is corrected using the Brown distortion model, with calibration parameters obtained via Astrometry.net. While this provides a reasonable approximation, the model does not account for all real-world optical and sensor imperfections.

Star detection is implemented using intensity thresholding followed by 4-connected region growing. Detected regions are processed to compute sub-pixel centroids using a weighted center-of-gravity approach. This method works well for clear star-like blobs but may be sensitive to noise and threshold selection.

For star identification, a small, reduced reference catalog (~60 Hipparcos-2 stars in the Gemini region) is used instead of a full-sky catalog. Triangle-based geometric features are generated from inter-star angular distances and matched using a hash-based approach. This simplifies the matching problem but limits robustness and scalability.

Candidate matches are validated by solving Wahba’s problem using SVD (Kabsch algorithm) to estimate rotation and minimize reprojection error. The final attitude is selected based on consistency across detected stars, and results are expressed as a rotation matrix and Euler angles.

Overall, this implementation is intended as a learning-oriented and proof-of-concept system, illustrating the core principles behind star trackers rather than a flight-ready or highly optimized solution.


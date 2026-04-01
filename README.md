<h1 align="center">
  <span style="color:#00FFFF;"> ٠ ࣪⭑Experimental CubeSat Star Tracker๋࣭ ⭑</span>
</h1>


## ✦ Summary ✦

This project presents a MATLAB-based prototype of a star tracker pipeline developed to explore the fundamentals of spacecraft attitude determination using star field images. The system operates on **BMP** images captured from an MT9P031 CMOS sensor and demonstrates key steps involved in real-world star tracker algorithms. <br>
The imaging process is approximated using an inverse pinhole camera model to convert 2D pixel coordinates into 3D unit vectors. Lens distortion is corrected using the Brown distortion model, with calibration parameters obtained via **Astrometry.net(nova.astrometry)(plate solving website)**. While this provides a reasonable approximation, the model does not account for all real-world optical and sensor imperfections. <br>
Star detection is implemented using intensity thresholding followed by 4-connected **region growing**. Detected regions are processed to compute sub-pixel centroids using a weighted center-of-gravity approach. This method works well for clear star-like blobs but may be sensitive to noise and threshold selection. <br>
For star identification, a small, reduced reference catalog (~60 **Hipparcos-2** stars in the Gemini region) is used instead of a full-sky catalog. Triangle-based geometric features are generated from inter-star angular distances and matched using a hash-based approach. This simplifies the matching problem but limits robustness and scalability. <br>
Candidate matches are validated by solving Wahba’s problem using SVD (Kabsch algorithm) to estimate rotation and minimize reprojection error. The final attitude is selected based on consistency across detected stars, and results are expressed as a rotation matrix and Euler angles. <br>
Overall, this implementation is intended as a **learning-oriented** and proof-of-concept system, illustrating the core principles behind star trackers rather than a flight-ready or highly optimized solution.

### Random Notes
⭑ I'll be dumping everything I EVER came across or tried to use in the **extra folder** - research papers, catalogues (reduced), files from Nova, etc.** <br>
⭑ A lot of things are yet to be fixed/changed since they affect accuracy or increase latency a lot (and there are definitely better modern methods), but I couldn't.
⭑ PS: Use the Tycho-2 Catalog for fainter stars' magnitudes if needed.** <br>
⭑ Also, tip: .fits format can't be directly opened, so I *generated* quick-fix Python scripts for it. They did the job, but weren’t maintained so use them carefully or        consider writing new ones.** <br>
⭑ Tried a few plate solving software… welp, turns out that’s a whole course on its own.** <br>
⭑ Currently, it takes ~50 sec to solve an image after partially parallelizing the tridb (earlier ~1:10 min) Ik that is really slow.** <br>
⭑ Finding images (with less distortion) is actually a big task in itself. Better to get in touch with someone who has worked on actual star trackers before for them, and to   also know what things/parameters are considered (insight and guidance)** <br>
⭑ Wanted to go with geometric voting algo (GVA), but ran into too many issues during implementation.**

### main.m
img = imread('images/bmp_4.bmp')<br>
img_double = im2double(img)<br>
img_copy = img_double<br>
subset = img_copy(4:4:end, 2:2:end)<br>
logical_subset = subset > threshold<br>
[star_region, img_copy] = region_growing(... )<br>
[cx_u, cy_u] = centroiding(... )<br>
[ux, uy, uz] = pixels_to_unit_vector(x, y)<br>
triangle_db = build_triangle_db(v_catalog, dbtol)<br>
matches = pattern_matching(... )<br>
[R_best, bestMatch, v_rotated] = attitude_determination(... )<br>

• Loads and converts image to double<br>
• Creates a subsampled grid for candidate detection<br>
• Applies threshold to identify bright pixels<br>
• Calls region growing to extract star regions<br>
• Calls centroiding to compute star centers<br>
• Converts pixel positions to unit vectors<br>
• Builds triangle database from catalog vectors<br>
• Performs pattern matching between detected and catalog stars<br>
• Computes final rotation using matched stars<br>

### region_growing.m
stack = [seed_r, seed_c]<br>
if img(r,c) > threshold<br>
region_pixels(end+1,:) = [r,c]<br>
img(r,c) = 0<br>
stack(end+1,:) = [r-1,c]<br>

• Initializes stack with seed pixel<br>
• Checks pixel intensity against threshold<br>
• Adds valid pixels to region list<br>
• Sets processed pixels to zero<br>
• Pushes neighboring pixels onto stack<br>
• Returns region only if size is within limits<br>

### centroiding.m
[~, idx_max] = max(intensities)<br>
cy_d = sum(win_cols .* win_intensities) / total_intensity<br>
cx_d = sum(win_rows .* win_intensities) / total_intensity<br>
[x_u, y_u] = distortion_correction(x_d, y_d)<br>

• Finds brightest pixel in region<br>
• Extracts local window around brightest pixel<br>
• Computes weighted centroid using intensities<br>
• Converts centroid from distorted to undistorted coordinates<br>

### distortion_correction.m
r2 = x.^2 + y.^2<br>
xu = x .* (1 + K1r2 + K2r2.^2) + P2*(r2 + 2x.^2) + 2P1.x.y<br>
yu = y . (1 + K1r2 + K2r2.^2) + P1(r2 + 2y.^2) + 2P2.*x.*y<br>

• Computes squared radius from center<br>
• Applies radial distortion terms<br>
• Applies tangential distortion terms<br>
• Outputs corrected pixel coordinates<br>

### pixels_to_unit_vector.m
alpha = (x_pix - xc) * ppx / f_mm<br>
beta = (y_pix - yc) * ppy / f_mm<br>
denom = sqrt(1 + alpha.^2 + beta.^2)<br>
ux = alpha / denom<br>
uy = beta / denom<br>
uz = 1 / denom<br>

• Shifts pixel coordinates relative to image center<br>
• Converts pixels to normalized image coordinates<br>
• Forms direction vector in camera frame<br>
• Normalizes vector to unit length<br>

### catalog_matching.m
ra = deg2rad(ra_deg)<br>
dec = deg2rad(dec_deg)<br>
x = cos(dec).*cos(ra)<br>
y = cos(dec).*sin(ra)<br>
z = sin(dec)<br>

• Reads catalog table from file<br>
• Converts RA and Dec strings to degrees<br>
• Converts degrees to radians<br>
• Computes Cartesian unit vectors<br>
• Returns vectors and star names<br>

### build_triangle_db.m
idx = nchoosek(1:N,3)<br>
feat = triangle_angles(tri)<br>
keys = hash_key(feat, tol)<br>
triangle_db(key) = {...}<br>

• Generates all triplets of catalog stars<br>
• Computes triangle features in parallel using parfor<br>
• Stores keys and triangle indices in temporary cell arrays<br>
• Builds hash map sequentially after parallel computation<br>

### triangle_angles.m
d12 = acosd(dot(v(1,:), v(2,:)))<br>
d23 = acosd(dot(v(2,:), v(3,:)))<br>
d31 = acosd(dot(v(3,:), v(1,:)))<br>
feat = sort([d12, d23, d31])<br>

• Computes angles between each pair of vectors<br>
• Uses dot product for angle calculation<br>
• Converts angles to degrees<br>
• Sorts angles to ensure consistent ordering<br>

### triangle_features.m
a = norm(v(2,:) - v(1,:))<br>
b = norm(v(3,:) - v(2,:))<br>
c = norm(v(1,:) - v(3,:))<br>
area = sqrt(s*(s-a)(s-b)(s-c))<br>

• Computes side lengths of triangle<br>
• Computes semi-perimeter and area<br>
• Normalizes lengths using area<br>
• Computes triangle angles<br>
• Combines length and angle features<br>

### hash_key.m
base = round(feat / tol)<br>
neighbor = base + [dx dy dz]<br>
keys{idx} = mat2str(neighbor)<br>

• Quantizes feature values using tolerance<br>
• Generates neighboring keys for robustness<br>
• Converts keys to string format<br>
• Returns list of candidate hash keys<br>

### hash_triangle_debug.m
triangle_indices = nchoosek(1:num_stars,3)<br>
dist_AB = acosd(dot(u,v))<br>
dist_round = round([...] / angle_round)<br>

• Generates triangles from detected stars<br>
• Computes angular distances for each triangle<br>
• Rounds values to create hash representation<br>
• Outputs numeric hash values for debugging<br>

### pattern_matching.m
det_idx = nchoosek(1:size(v_detected,1),3)<br>
feat = triangle_angles(tri)<br>
if isKey(triangle_db,key)<br>
[R, err] = verify_match(... )<br>

• Generates triangles from detected vectors<br>
• Computes triangle features<br>
• Looks up matching catalog triangles using hash<br>
• Verifies matches using rotation estimation<br>
• Applies consistency check using additional stars<br>

### verify_match.m
B = v_cat * v_det'<br>
[U,~,V] = svd(B)<br>
R = U * diag([1 1 det(U*V')]) * V'<br>

• Builds correlation matrix from matched vectors<br>
• Uses SVD to compute optimal rotation<br>
• Ensures proper rotation matrix<br>
• Applies rotation to detected vectors<br>
• Computes matching error<br>

### attitude_determination.m
H = v1' * v2<br>
[U,~,V] = svd(H)<br>
R = V * U'<br>
score = sum(min(dist,[],2) < 0.01)<br>

• Computes rotation for each match candidate<br>
• Applies rotation to all detected vectors<br>
• Computes distance to catalog vectors<br>
• Counts number of consistent matches<br>
• Selects best rotation based on score and error<br>




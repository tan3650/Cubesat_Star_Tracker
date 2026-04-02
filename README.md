<h1 align="center">
  <span style="color:#00FFFF;"> ٠ ࣪⭑ CubeSat Star Tracker (Algorithmic Exploration) ⭑٠ ࣪</span>
</h1>


## ✦ Summary ✦

This project is a MATLAB-based exploratory prototype aimed at understanding the basic pipeline of star trackers used for spacecraft attitude determination. It operates on BMP images captured from an MT9P031 CMOS sensor and focuses on experimenting with key steps such as star detection, centroiding, and pattern matching, rather than implementing a complete or optimized system. 

Pixel coordinates are converted into 3D unit vectors using an inverse pinhole camera model with assumed parameters (focal length and pixel pitch). This serves as a simplified approximation and does not fully capture real optical or sensor behavior.

Lens distortion effects were explored using the Brown–Conrady distortion model, with parameters obtained from Astrometry.net (plate solving). This was used to observe how distortion influences centroid accuracy, rather than perform precise calibration.

Star-like regions are identified using intensity thresholding followed by 4-connected region growing. Sub-pixel centroids are estimated using a weighted center-of-gravity approach. This method works reasonably well for clear star blobs but is sensitive to noise and threshold selection.

A small reference catalog (~60 Hipparcos-2 stars in the Gemini region) was used for initial experiments instead of a full-sky catalog. Triangle-based geometric features (angular distances) are generated and matched using a hash-based lookup approach. This simplifies matching but limits robustness and scalability.

Candidate matches are checked using Wahba’s problem (solved via SVD/Kabsch) to estimate rotation and observe consistency between detected and catalog stars. The resulting attitude is expressed as a rotation matrix and Euler angles.

Overall, this is a learning-oriented prototype intended to explore the core concepts behind star tracker pipelines, rather than a flight-ready or optimized implementation.

<img width="480" height="246" alt="Screenshot (994)" src="https://github.com/user-attachments/assets/5d02052a-dd08-4c9f-824c-c89a425cab40" /><img width="320" height="246" alt="Screenshot (430)" src="https://github.com/user-attachments/assets/2f5aec61-dffe-4798-b17d-8d1ca99f53d7" />


#### Random Notes
- I'll be dumping everything I came across or tried to use in the extra folder - research papers, reduced catalogs, files from Nova, etc.<br>
- Many parts still need improvement, especially where accuracy is low or latency is high (and there are definitely better modern methods I wasn’t able to implement). 
- Use the Tycho-2 catalog for fainter stars' magnitudes if needed.<br>
- Also, .fits files can’t be directly opened, so I generated quick-fix Python scripts for opening them. They worked, but I didn't bother maintaining/sorting the scripts       after their work was over. So, use them carefully or consider writing your own. (in extra/nova) <br>
- Tried a few plate-solving tools… turns out that’s a whole topic on its own. <br>
- Prtially parallelizing the triangle DB was a good decision (workers). <br>
- Finding good input images (with minimal distortion) is a challenge in itself. Try to find someone experienced with real star trackers for better insight into                parameters and constraints. <br>
- Initially planned to implement a geometric voting algorithm (GVA), but ran into multiple issues during implementation. format it so there is no text below bullet points when i put it in readme.
  
#### main.m
• Loads and converts image to double<br>
• Creates subsampled grid for candidate detection<br>
• Applies threshold to identify bright pixels<br>
• Calls region growing to extract star regions<br>
• Calls centroiding to compute star centers<br>
• Converts pixel positions to unit vectors<br>
• Builds triangle database from catalog vectors<br>
• Calls catalog_matching to load and convert catalog stars<br>
• Performs pattern matching between detected and catalog stars<br>
• Computes final rotation using matched stars<br>

#### region_growing.m
• Initializes stack with seed pixel<br>
• Checks pixel intensity against threshold<br>
• Adds valid pixels to region list<br>
• Sets processed pixels to zero<br>
• Pushes neighboring pixels onto stack<br>
• Returns region only if size is within limits<br>

#### centroiding.m
• Finds brightest pixel in region<br>
• Extracts local window around brightest pixel<br>
• Computes weighted centroid using intensities<br>
• Converts centroid from distorted to undistorted coordinates<br>

#### distortion_correction.m
• Computes squared radius from center<br>
• Applies radial distortion terms<br>
• Applies tangential distortion terms<br>
• Outputs corrected pixel coordinates<br>

#### pixels_to_unit_vector.m
• Shifts pixel coordinates relative to image center<br>
• Converts pixels to normalized image coordinates<br>
• Forms direction vector in camera frame<br>
• Normalizes vector to unit length<br>

#### catalog_matching.m
• Reads catalog table from file<br>
• Converts RA and Dec strings to degrees<br>
• Converts degrees to radians<br>
• Computes Cartesian unit vectors<br>
• Returns vectors and star names<br>

#### build_triangle_db.m 
• Uses the catalog vectors generated to:<br>
• Generate all triplets of catalog stars<br> (||)
• Compute angular features for each triangle<br>
• Convert features to hash keys<br>
• Stores triangle indices in hash map<br>

#### triangle_angles.m
• Computes angles between each pair of vectors<br>
• Uses dot product for angle calculation<br>
• Converts angles to degrees<br>
• Sorts angles to ensure consistent ordering<br>

#### triangle_features.m
• Computes side lengths of triangle<br>
• Computes semi-perimeter and area<br>
• Normalizes lengths using area<br>
• Computes triangle angles<br>
• Combines length and angle features<br>

#### hash_key.m
• Quantizes feature values using tolerance<br>
• Generates neighboring keys for robustness<br>
• Converts keys to string format<br>
• Returns list of candidate hash keys<br>

#### hash_triangle_debug.m
• Generates triangles from detected stars<br>
• Computes angular distances for each triangle<br>
• Rounds values to create hash representation<br>
• Outputs numeric hash values for debugging<br>

#### pattern_matching.m
• Generates triangles from detected vectors<br>
• Computes triangle features<br>
• Looks up matching catalog triangles using hash<br>
• Verifies matches using rotation estimation<br>
• Applies consistency check using additional stars<br>

#### verify_match.m
• Builds correlation matrix from matched vectors<br>
• Uses SVD to compute optimal rotation<br>
• Ensures proper rotation matrix<br>
• Applies rotation to detected vectors<br>
• Computes matching error<br>

#### attitude_determination.m
• Computes rotation for each match candidate<br>
• Applies rotation to all detected vectors<br>
• Computes distance to catalog vectors<br>
• Counts number of consistent matches<br>
• Selects best rotation based on score and error<br>

-----------------------------------------------------------------------
### image_plane.m (no need after updating pixtvect) but otherwise
• Converts pixel coordinates into image plane coordinates<br>
• Shifts coordinates relative to principal point<br>
• Scales using camera parameters<br>
• Prepares coordinates for geometric transformations<br>

### hash_triangle_matching.m (old)
• Matches detected triangle hash keys with catalog hash keys<br>
• Retrieves candidate catalog triangles from hash database<br>
• Compares detected and catalog triangle correspondences<br>
• Outputs possible triangle matches for further validation<br>



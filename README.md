<h1 align="center">
  <span style="color:#00FFFF;"> ٠ ࣪⭑CubeSat Star Tracker๋࣭ ⭑</span>
</h1>



## ✦ Overview and Purpose

A star tracker is an optical device that determines the attitude (orientation) of a satellite by observing stars. Since the positions of stars are known with extremely high accuracy from astronomical catalogues, a spacecraft can use them as fixed reference points in space. This system captures an image of the star field, detects the apparent positions of stars in the spacecraft’s reference frame, and matches them against a known catalogue to compute the spacecraft’s orientation.

This project focuses on developing a compact, efficient, and reliable star tracker suitable for CubeSat missions, with emphasis on practical implementation and early-stage validation.

---

## ✦ Optical Design and Sensor Selection

<div style="background: linear-gradient(135deg, #00FFFF, #8A2BE2, #FF69B4); padding: 12px; border-radius: 12px; color: black;">

The system is built around the <b>MT9P031-D 5 MP CMOS image sensor</b>, chosen for its compactness, low power consumption, and global shutter capability, which prevents motion distortion. It provides CCD-like image quality in terms of signal-to-noise ratio and low-light sensitivity while maintaining the integration advantages of CMOS sensors.

The sensor has an active imaging area of 5.70 mm × 4.28 mm with a diagonal of 7.13 mm and a pixel size of 4.4 µm. It operates in 4× binning mode, reducing the effective resolution to approximately 646 × 486 pixels. This improves light sensitivity, reduces noise, and decreases computational load, allowing faster onboard processing.

</div>

---

## ✦ Image Processing Pipeline

<span style="color:#DA70D6;">
The image processing pipeline begins by converting raw sensor data into a suitable format, typically floating-point, followed by a threshold-based detection step to identify potential star pixels. Region growing is then applied to group connected high-intensity pixels, effectively isolating individual stars while preventing duplicate detections by removing already processed regions.  
</span>

<br>

<span style="color:#9370DB;">
Once stars are detected, centroiding is performed using a weighted center-of-gravity approach around the brightest pixel, enabling sub-pixel accuracy in determining star positions. These coordinates initially include optical distortion, which is corrected using Brown’s distortion model along with SIP (Simple Imaging Polynomial) coefficients to produce undistorted pixel coordinates.  
</span>

<br>

<span style="color:#FF69B4;">
Finally, the corrected 2D coordinates are projected into 3D unit vectors in the spacecraft body frame using the inverse pinhole camera model. These vectors form the basis for attitude determination.  
</span>

---

## ✦ Star Matching Algorithm

<div style="background: linear-gradient(135deg, #8A2BE2, #DA70D6, #FF69B4); padding: 12px; border-radius: 12px; color: white;">

The star identification method is inspired by the Pyramid algorithm but optimized using a hash-based triangle matching approach for computational efficiency. Triangles are formed from groups of three detected stars, and invariant geometric features such as angular separations and internal angles are calculated.

These features are converted into hash keys and compared against a precomputed catalogue of triangle features. When a match is found, it is validated through an attitude consistency check to eliminate false positives. Because the geometric features are invariant to rotation and translation, the method remains robust under different spacecraft orientations while maintaining fast identification performance.

</div>

---

## ✦ Attitude Determination

<span style="color:#00CED1;">
Attitude determination is performed by comparing detected star vectors with their corresponding catalogue vectors and solving Wahba’s problem to find the optimal rotation. Two approaches are considered: the SVD-based Kabsch algorithm and the QUEST (Quaternion ESTimator) algorithm.  
</span>

<br>

<span style="color:#BA55D3;">
The QUEST algorithm is preferred due to its numerical stability and computational efficiency. It constructs Davenport’s K matrix from the vector correspondences and computes the eigenvector corresponding to the largest eigenvalue, yielding the optimal quaternion representation of the spacecraft’s orientation. This quaternion can be directly used in attitude filters or converted into a rotation matrix if required.  
</span>

---

## ✦ Performance and Results

<div style="background: linear-gradient(135deg, #00FFFF, #9370DB, #FF69B4); padding: 12px; border-radius: 12px; color: black;">

Testing shows that the system produces consistent and repeatable results using the baseline pipeline, with reliable star identification and stable attitude estimation across different test images. Initial results indicate attitude determination errors within a few arcminutes when using a smaller catalogue, which meets the requirements for early-stage validation.

</div>

---

## ✦ Limitations and Future Improvements

<span style="color:#DDA0DD;">
The primary factors affecting accuracy include centroid precision, optical calibration, and catalogue quality. Potential sources of error include sensor noise, optical distortion, inaccuracies in the catalogue, and mismatches in dense star fields.  
</span>

<br>

<span style="color:#FF69B4;">
Future improvements will focus on enhanced preprocessing, better calibration techniques, larger and optimized star catalogues, and integration of advanced matching strategies to improve both accuracy and robustness for real mission conditions.  
</span>

---



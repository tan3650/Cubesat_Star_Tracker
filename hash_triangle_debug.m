function [triangle_hash_keys] = hash_triangle_debug(star_unit_vectors, angle_round)
%HASH_TRIANGLE_DEBUG Compute and print numeric hash keys of detected triangles

num_stars = size(star_unit_vectors,1);
triangle_indices = nchoosek(1:num_stars,3);
triangle_hash_keys = zeros(size(triangle_indices,1),1);

for k = 1:size(triangle_indices,1)
    idx = triangle_indices(k,:);
    u = star_unit_vectors(idx(1),:);
    v = star_unit_vectors(idx(2),:);
    w = star_unit_vectors(idx(3),:);

    % Angular distances in degrees
    dist_AB = acosd(dot(u,v));
    dist_BC = acosd(dot(v,w));
    dist_CA = acosd(dot(w,u));

    % Round and compute numeric hash
    dist_round = round([dist_AB, dist_BC, dist_CA] / angle_round);
    triangle_hash_keys(k) = dist_round(1)*1e8 + dist_round(2)*1e4 + dist_round(3);

    % Print hash for debug
    fprintf('Detected triangle %d: hash = %d, angular distances = [%.3f, %.3f, %.3f]\n', ...
        k, triangle_hash_keys(k), dist_AB, dist_BC, dist_CA);
end
end

function triangle_db = build_triangle_db(v_catalog, tol)
    idx = nchoosek(1:size(v_catalog, 1), 3);
    triangle_db = containers.Map;

    for i = 1:size(idx, 1)
        tri = v_catalog(idx(i,:), :);
        feat = triangle_angles(tri);
        keys = hash_key(feat, tol);  % Generate multiple nearby hash bins

        for k = 1:length(keys)
            key = keys{k};
            if isKey(triangle_db, key)
                temp = triangle_db(key);      % Get the current list
                temp{end+1} = idx(i,:);       % Append new triangle
                triangle_db(key) = temp;      % Store updated list
            else
                triangle_db(key) = {idx(i,:)};  % Initialize with one triangle
            end
        end
    end
end

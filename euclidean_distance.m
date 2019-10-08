a= dlmread('/home/philipp/alzheimers/neurodegeneration-forecast/atlases/combined_atlas_coord_list.txt');

center = zeros(571,3);

for i = 1:571
    center(i,:) = mean(a(a(:,1)==i,2:4));
end
distances = zeros(571,571);
for i = 1:571
    for j = 1:571
        distances(i,j) = norm(center(i,:) - center(j,:));
    end
end

%dlmwrite('euclidean_distances.txt',distances,' ');

distances  = distances./min(distances(distances>0));
distances = distances.^-1;
distances(isinf(distances)) = 0;

%dlmwrite('euclidean_adjecency.txt',distances,' ');

sorted = sort(distances(:));
threshold_value = sorted(end-round(6*571));
distances(distances<threshold_value) = 0;

dlmwrite('euclidean_adjecency_6neighbors.txt',distances,' ');

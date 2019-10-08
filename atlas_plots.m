function atlas_plots()
  #plot_diameter('combined_atlas',500,3000)
  plot_diameter('combined_atlas_new_labels_2018_09_17',500,3000)
  #plot_diameter('combined_atlas400',500,3000)
  #plot_diameter('combined_atlas390',500,3000)
  #plot_diameter('combined_atlas380',500,3000)
  #plot_diameter('combined_atlas370',500,3000)
  #plot_diameter('naive_combined',0,140000)
  #plot_hist('combined_atlas',0.19)
  #plot_hist('naive_combined',0.33)
endfunction

function plot_diameter (name,xrange_low,xrange_high)
  figure
  fileID = fopen([name '_labels.txt']);
  C = textscan(fileID,'%f %s %f %f\n','delimiter',',');
  plot(C{3}/1000,C{4},'.') 
  x = linspace(xrange_low,xrange_high);
  y = (3*x.^(2/3)).^(1/2);
  hold on
  plot(x/1000,y)
  y2 = x.^(1/3)*3/4/pi*2;
  plot(x/1000,y2)
  xlabel('Volume [ml]')
  ylabel('Diameter [mm]')
  legend('Regions','Cubes','Spheres','location','Northwest')
  print([name '_diameters'],"-dpng")
  close all
endfunction

function plot_hist (name,ypos)
  figure
  fileID = fopen([name '_labels.txt']);
  C = textscan(fileID,'%f %s %f %f\n','delimiter',',');
  hist(C{3}/1090,nbins=30,norm=1)
  hold on
  plot(mean(C{3})/1000,ypos,'bx')
  plot([mean(C{3})/1000-std(C{3})/1000,mean(C{3})/1000+std(C{3})/1000],[ypos,ypos],'b-')
  
  xlabel('Volume [ml]')
  ylabel('Probability')
  legend('Regions','Mean','Std','location','NorthEast')
  print([name '_hist'],"-dpng")
  close all
  endfunction

Rex::Socket::SwitchBoard.each do |route|
	print_good ("#{route.subnet}")
	print_status("Starting SMB Scan")
	File.write('/root/Documents/subnetip.txt', route.subnet)
	
	
end
#TODO find a why to stop ms17 scan when found (in console or in scan.rb)

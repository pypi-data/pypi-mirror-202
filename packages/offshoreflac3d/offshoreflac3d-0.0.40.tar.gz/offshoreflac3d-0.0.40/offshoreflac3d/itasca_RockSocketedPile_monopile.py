import itasca as it
it.command("python-reset-state false")

def monopile():
	it.command("model new")
	it.command("model restore 'Initial'")
	
	command = '''
	zone cmodel assign elastic range position-z [layerings(1)] [layerings(2)]
	
	zone cmodel assign elastic range group 'pile' slot 'pile' position-z [layerings(1)] [layerings(1)-length]
	zone cmodel assign mohr-coulomb range group 'grouting_1' slot 'pile' position-z [layerings(1)] [layerings(1)-length]
	zone cmodel assign mohr-coulomb range group 'grouting_2' slot 'pile' position-z [layerings(1)] [thick_grouting_depth]
	zone group 'grouting' slot 'grouting' range group 'grouting_1' slot 'pile' position-z [layerings(1)] [layerings(1)-length]
	zone group 'grouting' slot 'grouting' range group 'grouting_2' slot 'pile' position-z [layerings(1)] [thick_grouting_depth]
	
	zone delete range group 'grouting_1' slot 'pile' position-z [layerings(1)] [layerings(2)]
	zone delete range group 'grouting_2' slot 'pile' position-z [layerings(1)] [layerings(2)]
	zone delete range group 'BC_1' slot 'BC' position-z [layerings(1)] [layerings(2)]
	zone delete range group 'BC_2' slot 'BC' position-z [layerings(1)] [layerings(2)]
	zone delete range group 'BC_3' slot 'BC' position-z [layerings(1)] [layerings(2)]
	
	zone delete range position-z [layerings(1)] [Z_list(1)-scour_depth] group 'pile' slot 'pile' not
	
	zone delete range group "Central" slot "pile" position-z [layerings(1)] [layerings(1)-length]
	'''
	it.command(command)
	
	command = '''
	fish define  thickness_change
		loop local i (1,list.size(in_range)-1)
			loop foreach local gp gp.list
				if gp.pos.z(gp) < in_range(i) & gp.pos.z(gp) > in_range(i+1) then
					local s = gp.pos.x(gp)^2 + gp.pos.y(gp)^2
					if s > 0.98 & s < 1.02 then
						local sin = gp.pos.x(gp)
						local cos = gp.pos.y(gp)
						gp.pos.x(gp) = (radius-thickness(i))*sin
						gp.pos.y(gp) = (radius-thickness(i))*cos
					endif
				endif
			endloop
		endloop
	end
	'''
	it.command(command)
	it.fish.call_function("thickness_change")
	
	
	command = '''
	zone property density 7.85 young 2.1e8 poisson 0.2 range group 'pile' slot 'pile' cmodel 'elastic'
	zone property density 2.45 young 0.40e8 poisson 0.20 cohesion 4.4e3 friction 63 tension 6e3 range group 'grouting_1' slot 'pile' position-z [layerings(1)] [layerings(1)-length]
	zone property density 2.45 young 0.40e8 poisson 0.20 cohesion 4.4e3 friction 63 tension 6e3 range group 'grouting_2' slot 'pile' position-z [layerings(1)] [thick_grouting_depth]
	'''
	it.command(command)
	
	command = '''
	zone group 'NoPile' slot 'Default' range group 'pile' slot 'pile' position-z [layerings(1)-length] [layerings(-1)]
	
	zone interface 'grouting_soil_interaction' create by-face separate ...
			range group 'grouting_2' slot 'pile' group 'BC_1' slot 'BC' position-z [layerings(1)] [thick_grouting_depth]
	zone interface 'grouting_soil_interaction' create by-face separate ...
			range group 'grouting_1' slot 'pile' group 'grouting_2' slot 'pile' position-z [thick_grouting_depth] [grouting_soil_interaction]
	zone interface 'pile_soil_interaction' create by-face separate ...
			range group 'grouting_1' slot 'pile' group 'pile' slot 'pile' position-z [layerings(1)] [layerings(1)-length]
	zone interface 'pile_soil_interaction_toe' create by-face separate ...
			range group 'NoPile' slot 'Default' group 'pile' slot 'pile' position-z [layerings(1)-length]
	
	zone interface node property stiffness-normal 2e9 stiffness-shear 2e9 friction 22
	zone interface node property stiffness-normal 2e9 stiffness-shear 2e9 friction 26.5 cohesion 150 range group 'pile_soil_interaction'
	'''
	it.command(command)
	
	
	it.command("model solve ratio 1e-6")
	it.command("model save 'Monopile'")
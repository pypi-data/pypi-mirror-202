import itasca as it
it.command("python-reset-state false")

def initializing():

	it.command("model restore 'Model'")
	it.command("model large-strain off")
	it.command("model gravity [gravity]")
	
	command = '''
	zone cmodel assign mohr-coulomb
	zone cmodel assign null range position-z [layerings(1)] [Z_list(1)]
	'''
	it.command(command)
	
	command = '''
	fish define assigning_properties
		loop local i (1,list.size(Z_list)-1)
            command
                zone property density [density(i)] range group [string.build("Soil_%1",i)]
                zone property young [elastic(i)] range group [string.build("Soil_%1",i)]
                zone property poisson [poisson(i)] range group [string.build("Soil_%1",i)]
                zone property cohesion [cohesion(i)] range group [string.build("Soil_%1",i)]
                zone property friction [friction(i)] range group [string.build("Soil_%1",i)]
                zone property tension [cohesion(i)*0.5+friction(i)*0.3] range group [string.build("Soil_%1",i)]
                zone initialize-stresses ratio [poisson(i)/(1-poisson(i))] range group [string.build("Soil_%1",i)]
            endcommand
		endloop
	end
	'''
	it.command(command)
	it.fish.call_function("assigning_properties")
	
	command = '''
	fish define setting_boundary
		loop foreach local _gp gp.list
			if math.round(gp.pos.z(_gp)) == Z_list(list.size(Z_list)) then
				gp.fix.x(_gp) = true
				gp.fix.y(_gp) = true
				gp.fix.z(_gp) = true
			else if math.round((gp.pos.x(_gp))^2 + (gp.pos.y(_gp))^2) == math.round(R_list(-1)^2) then
				gp.fix.x(_gp) = true
				gp.fix.y(_gp) = true
			endif
		endloop
	end
	'''
	it.command(command)
	it.fish.call_function("setting_boundary")
	
	it.command("model solve ratio 1e-6")
	it.command("model save 'Initial'")
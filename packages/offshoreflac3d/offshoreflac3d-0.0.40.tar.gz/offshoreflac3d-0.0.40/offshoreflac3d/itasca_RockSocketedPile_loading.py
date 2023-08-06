import itasca as it
it.command("python-reset-state false")

def loading(loads_cc,loads_tt,pile_top,Z_list,option):

    it.command("model restore 'Monopile'")
    
    command = '''
    zone gridpoint initialize displacement 0 0 0
    zone gridpoint initialize velocity 0 0 0
    
    zone history displacement position [radius] 0 [pile_top]
    zone history displacement position [-radius] 0 [pile_top]
    '''
    it.command(command)
    
    command = '''
    fish define loading(loads,dir,pos)
        local N = Jx = Jy = Jz = 0
        loop foreach local gp gp.list
            if gp.pos.z(gp) == pos then 
                N = N + 1
                Jx = Jx + gp.pos.x(gp)^2
            endif
        endloop
        Jy = Jx
        Jz = Jx + Jy
        
        io.out(Jx)
        
        local load_gp = loads / N
        
        loop foreach gp gp.list
            if gp.pos.z(gp) == pos then 
                if dir == 1 then gp.force.load.x(gp) = load_gp
                if dir == 2 then gp.force.load.y(gp) = load_gp
                if dir == 3 then gp.force.load.z(gp) = load_gp
                if dir == 4 then 
                    load_gp = loads*gp.pos.y(gp)/Jx
                    local load_gp_final = gp.force.load.z(gp) + load_gp
                    gp.force.load.z(gp) = load_gp_final
                endif
                if dir == 5 then 
                    load_gp = -loads*gp.pos.x(gp)/Jy
                    load_gp_final = gp.force.load.z(gp) + load_gp
                    gp.force.load.z(gp) = load_gp_final
                endif
                if dir == 6 then 
                    r = math.sqrt(gp.pos.x(gp)^2+gp.pos.y(gp)^2)
                    theta = math.asin(gp.pos.y(gp)/r)
                    load_n = loads*r/Jy
                    if gp.pos.x(gp) < 0 then
                        load_n_final_x = gp.force.load.x(gp) + -load_n*math.sin(theta)
                        load_n_final_y = gp.force.load.y(gp) + -load_n*math.cos(theta)
                        gp.force.load.x(gp) = load_n_final_x
                        gp.force.load.y(gp) = load_n_final_y
                    else
                        load_n_final_x = gp.force.load.x(gp) + -load_n*math.sin(theta)
                        load_n_final_y = gp.force.load.y(gp) +  load_n*math.cos(theta)
                        gp.force.load.x(gp) = load_n_final_x
                        gp.force.load.y(gp) = load_n_final_y
                    endif
                endif
            endif
        endloop
    end
    ;;
    fish define deformation_components
        local gp_1 = gp.near( radius,0,Z_list(1))
        local gp_2 = gp.near(-radius,0,Z_list(1))
        global x_disp = (gp.disp.x(gp_1)+gp.disp.x(gp_2))/2.0
        global y_disp = (gp.disp.y(gp_1)+gp.disp.y(gp_2))/2.0
        global z_disp = (gp.disp.z(gp_1)+gp.disp.z(gp_2))/2.0
        global rotation = math.abs(gp.disp.z(gp_1)-gp.disp.z(gp_2))/(2.0*radius)
        global torsion = math.abs(gp.disp.y(gp_1)-gp.disp.y(gp_2))/(2.0*radius)
    end
    ;
    fish define ploting_option(saving)
        if saving == 'Final_cc' |  saving == 'Final_tt' then
            system.command("plot 'pile_mises_stress' export bitmap filename [string.build(saving + '_pile_mises_stress')]")
            system.command("plot 'pile_deformation_x' export bitmap filename [string.build(saving + '_pile_deformation_x')]")
            system.command("plot 'pile_deformation_z' export bitmap filename [string.build(saving + '_pile_deformation_z')]")
            system.command("plot 'grouting_min' export bitmap filename [string.build(saving + '_grouting_min')]")
            system.command("plot 'grouting_max' export bitmap filename [string.build(saving + '_grouting_max')]")
            system.command("plot 'soil_state' export bitmap filename [string.build(saving + '_soil_state')]")
            system.command("plot 'soil_deformation' export bitmap filename [string.build(saving + '_soil_deformation')]")
        endif
    end
    '''
    it.command(command)
    
    
    ############compresssion case
    it.command("model save 'temp'")
    
    if option[0] == 'Bearing Capacity':
        print(option[0])
        it.command("model restore 'temp'")
        
        for i in range(0,6):
            it.fish.call_function("loading",(loads_cc[i],i+1,pile_top))
        it.command("[global saving = 'Final_cc']")
        it.command("model solve ratio 1e-5")
        it.fish.call_function("deformation_components")
        it.fish.call_function("ploting_option(saving)")
        it.command("model save [saving]")
        
        
        # #############tension case
        it.command("model restore 'temp'")
        
        for i in range(0,6):
            it.fish.call_function("loading",(loads_tt[i],i+1,pile_top))
        
        it.command("[global saving = 'Final_tt']")
        it.command("model solve ratio 1e-5")
        it.fish.call_function("deformation_components")
        it.fish.call_function("ploting_option(saving)")
        it.command("model save [saving]")
    
    if option[1] == 'Stiffness':
        print(option[1])
        #############deformation components
        it.command("model restore 'temp'")
        
        it.fish.call_function("loading",(loads_cc[0],1,Z_list[0]))
        
        it.command("[global saving = 'Final_cc_x']")
        it.command("model solve ratio 1e-5")
        it.fish.call_function("deformation_components")
        it.fish.call_function("ploting_option(saving)")
        it.command("model save [saving]")
        
        #############deformation components
        it.command("model restore 'temp'")
        
        it.fish.call_function("loading",(loads_cc[2],3,Z_list[0]))
        
        it.command("[global saving = 'Final_cc_z']")
        it.command("model solve ratio 1e-5")
        it.fish.call_function("deformation_components")
        it.fish.call_function("ploting_option(saving)")
        it.command("model save [saving]")
        
        #############deformation components
        it.command("model restore 'temp'")
        print(loads_cc[4])
        loads_cc[4] = loads_cc[4] + (pile_top-Z_list[0])*loads_cc[0]
        print(loads_cc[4])
        it.fish.call_function("loading",(loads_cc[4],5,Z_list[0]))
        
        it.command("[global saving = 'Final_cc_my']")
        it.command("model solve ratio 1e-5")
        it.fish.call_function("deformation_components")
        it.fish.call_function("ploting_option(saving)")
        it.command("model save [saving]")
        
        #############deformation components
        it.command("model restore 'temp'")
        
        it.fish.call_function("loading",(loads_cc[5],6,Z_list[0]))
        
        it.command("[global saving = 'Final_cc_z']")
        it.command("model solve ratio 1e-5")
        it.fish.call_function("deformation_components")
        it.fish.call_function("ploting_option(saving)")
        it.command("model save [saving]")

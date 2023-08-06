import itasca as it
it.command("python-reset-state false")

def model():
    command = '''
    ;;
    extrude set select "geometry"
    extrude point create (0,0)
    extrude point create (0,[R_list(1)])
    extrude point create (0,[R_list(2)])
    extrude point create (0,[R_list(3)])
    extrude point create (0,[R_list(4)])
    extrude point create (0,[R_list(5)])
    extrude point create (0,[R_list(6)])
    extrude point create (0,[R_list(7)])
    extrude point create ([R_list(1)],0)
    extrude point create ([R_list(2)],0)
    extrude point create ([R_list(3)],0)
    extrude point create ([R_list(4)],0)
    extrude point create ([R_list(5)],0)
    extrude point create ([R_list(6)],0)
    extrude point create ([R_list(7)],0)

    extrude edge create by-points 1 2 type simple
    extrude edge create by-points 2 3 type simple
    extrude edge create by-points 3 4 type simple
    extrude edge create by-points 4 5 type simple
    extrude edge create by-points 5 6 type simple
    extrude edge create by-points 6 7 type simple
    extrude edge create by-points 7 8 type simple

    extrude edge create by-points 1 9 type simple
    extrude edge create by-points 9 10 type simple
    extrude edge create by-points 10 11 type simple
    extrude edge create by-points 11 12 type simple
    extrude edge create by-points 12 13 type simple
    extrude edge create by-points 13 14 type simple
    extrude edge create by-points 14 15 type simple

    extrude edge id 1 split ([0],[radius/3])
    extrude edge id 8 split ([radius/3],[0])
    extrude point create ([radius/3],[radius/3])

    extrude point create ([R_list(1)*math.cos((45)/180*math.pi)],[R_list(1)*math.sin((45)/180*math.pi)])
    extrude point create ([R_list(2)*math.cos((45)/180*math.pi)],[R_list(2)*math.sin((45)/180*math.pi)])
    extrude point create ([R_list(3)*math.cos((45)/180*math.pi)],[R_list(3)*math.sin((45)/180*math.pi)])
    extrude point create ([R_list(4)*math.cos((45)/180*math.pi)],[R_list(4)*math.sin((45)/180*math.pi)])
    extrude point create ([R_list(5)*math.cos((45)/180*math.pi)],[R_list(5)*math.sin((45)/180*math.pi)])
    extrude point create ([R_list(6)*math.cos((45)/180*math.pi)],[R_list(6)*math.sin((45)/180*math.pi)])
    extrude point create ([R_list(7)*math.cos((45)/180*math.pi)],[R_list(7)*math.sin((45)/180*math.pi)])

    extrude edge create by-points 16 18 type simple
    extrude edge create by-points 17 18 type simple

    extrude edge create by-points 02 19 type simple
    extrude edge create by-points 09 19 type simple
    extrude edge create by-points 18 19 type simple

    extrude edge create by-points 03 20 type simple
    extrude edge create by-points 10 20 type simple
    extrude edge create by-points 19 20 type simple

    extrude edge create by-points 04 21 type simple
    extrude edge create by-points 11 21 type simple
    extrude edge create by-points 20 21 type simple

    extrude edge create by-points 05 22 type simple
    extrude edge create by-points 12 22 type simple
    extrude edge create by-points 21 22 type simple

    extrude edge create by-points 06 23 type simple
    extrude edge create by-points 13 23 type simple
    extrude edge create by-points 22 23 type simple

    extrude edge create by-points 07 24 type simple
    extrude edge create by-points 14 24 type simple
    extrude edge create by-points 23 24 type simple

    extrude edge create by-points 08 25 type simple
    extrude edge create by-points 15 25 type simple
    extrude edge create by-points 24 25 type simple

    extrude edge id 20 control-point add ([R_list(1)*math.cos((22.5)/180*math.pi)],[R_list(1)*math.sin((22.5)/180*math.pi)])
    extrude edge id 23 control-point add ([R_list(2)*math.cos((22.5)/180*math.pi)],[R_list(2)*math.sin((22.5)/180*math.pi)])
    extrude edge id 26 control-point add ([R_list(3)*math.cos((22.5)/180*math.pi)],[R_list(3)*math.sin((22.5)/180*math.pi)])
    extrude edge id 29 control-point add ([R_list(4)*math.cos((22.5)/180*math.pi)],[R_list(4)*math.sin((22.5)/180*math.pi)])
    extrude edge id 32 control-point add ([R_list(5)*math.cos((22.5)/180*math.pi)],[R_list(5)*math.sin((22.5)/180*math.pi)])
    extrude edge id 35 control-point add ([R_list(6)*math.cos((22.5)/180*math.pi)],[R_list(6)*math.sin((22.5)/180*math.pi)])
    extrude edge id 38 control-point add ([R_list(7)*math.cos((22.5)/180*math.pi)],[R_list(7)*math.sin((22.5)/180*math.pi)])

    extrude edge id 19 control-point add ([R_list(1)*math.cos((67.5)/180*math.pi)],[R_list(1)*math.sin((67.5)/180*math.pi)])
    extrude edge id 22 control-point add ([R_list(2)*math.cos((67.5)/180*math.pi)],[R_list(2)*math.sin((67.5)/180*math.pi)])
    extrude edge id 25 control-point add ([R_list(3)*math.cos((67.5)/180*math.pi)],[R_list(3)*math.sin((67.5)/180*math.pi)])
    extrude edge id 28 control-point add ([R_list(4)*math.cos((67.5)/180*math.pi)],[R_list(4)*math.sin((67.5)/180*math.pi)])
    extrude edge id 31 control-point add ([R_list(5)*math.cos((67.5)/180*math.pi)],[R_list(5)*math.sin((67.5)/180*math.pi)])
    extrude edge id 34 control-point add ([R_list(6)*math.cos((67.5)/180*math.pi)],[R_list(6)*math.sin((67.5)/180*math.pi)])
    extrude edge id 37 control-point add ([R_list(7)*math.cos((67.5)/180*math.pi)],[R_list(7)*math.sin((67.5)/180*math.pi)])

    extrude edge id 19 type arc
    extrude edge id 22 type arc
    extrude edge id 25 type arc
    extrude edge id 28 type arc
    extrude edge id 31 type arc
    extrude edge id 34 type arc
    extrude edge id 37 type arc

    extrude edge id 20 type arc
    extrude edge id 23 type arc
    extrude edge id 26 type arc
    extrude edge id 29 type arc
    extrude edge id 32 type arc
    extrude edge id 35 type arc
    extrude edge id 38 type arc

    extrude edge size 7; range id-list 14 17 20 23 13 16 19 22
    extrude edge size 1 range id-list 2 3 4 24 27 30 9 10 11

    ;extrude edge ratio 1.1 range id-list 2 3 4 6 7 8 18 21 24


    extrude block create automatic

    extrude block group "pile" slot "pile" range id-list 8 14
    extrude block group "grouting_1" slot "pile" range id-list 7 13
    extrude block group "grouting_2" slot "pile" range id-list 6 12

    extrude block group "Central" slot "pile" range id-list 9 15 2

    extrude block group "BC_1" slot "BC" range id-list 5 11
    extrude block group "BC_2" slot "BC" range id-list 4 10
    extrude block group "BC_3" slot "BC" range id-list 3 1

    extrude segment index 1 length 0.1 size 1 group "basic" slot "Default"

    extrude set system u-axis (1,0,0) v-axis (0,1,0)
    extrude set system origin 0 0 [layerings(1)]
    
    ;program call 'geometry' suppress
    zone generate from-extrude
    zone reflect dip-direction 90 dip 90
    zone reflect dip-direction 180 dip 270
    zone select
    '''
    it.command(command)
    
    command = '''
    fish define copying_model
        loop local i (2,list.size(layerings)-1)
            system.command('zone copy 0 0 [layerings(i)-layerings(1)] merge on range selected')
        endloop
    end
    '''
    it.command(command)
    it.fish.call_function("copying_model")
    
    command = '''
    fish define merging_densifying_all
        loop local i (1,list.size(layerings)-1)
            system.command('zone gridpoint initialize position-z [layerings(i+1)] range position-z [layerings(i)-0.1-0.05] [layerings(i)-0.1+0.05]')
            if math.round(layerings(i)-layerings(i+1)) == 1 then
                ;continue
                system.command('zone densify global segments 1 1 3 range position-z [layerings(i)] [layerings(i+1)]')
            else if math.round(layerings(i)-layerings(i+1)) == 0 then
                system.command('zone densify global segments 1 1 2 range position-z [layerings(i)] [layerings(i+1)]')
            else
                system.command('zone densify global segments 1 1 [math.round(layerings(i)-layerings(i+1))*3] range position-z [layerings(i)] [layerings(i+1)]')
            endif
        endloop
    end
    '''
    it.command(command)
    it.fish.call_function("merging_densifying_all")
    
    command = '''
    fish define naming_soils
        loop local i (1,list.size(Z_list)-1)
            system.command('zone group [string.build("Soil_%1",i)] slot "soil" range position-z [Z_list(i)] [Z_list(i+1)]')
        endloop
    end
    '''
    it.command(command)
    it.fish.call_function("naming_soils")
    
    it.command("zone attach by-face tolerance-absolute 0.1")
    it.command("model save 'Model'")
from Euhforia_Run import *
from tqdm.auto import tqdm
import os

root_path = os.path.join(os.path.expanduser(
    "~"), "local_thesis", "scratch_11_4")
euhforia_events_path = os.path.join(
    root_path, "euhforia_events")

doPlus, doMinus = True, True

for run_name in tqdm(ALL_FOLDERS):
    run_path = os.path.join(euhforia_events_path, run_name, "dat")
    run = Euhforia_Run(run_path, run_name, os.path.join(data_path_from_root(
        root_path), "scaled_bclt_sq_v2"), os.path.join(gfx_path_from_root(root_path), "scaled_bclt_sq_v2"), max_size=0)

    # add logger for this part
    logger = run.log.getChild("fluxCalc_and_visualize")
    tp.macro.execute_command(
        '''$!FrameControl ActivateByNumber Frame = 1''')

    # alter data
    tp.data.operate.execute_equation(equation='{bz_eq}=-{bclt}',
                                     ignore_divide_by_zero=True)
    tp.data.operate.execute_equation(equation='{scaled_bz_sq}=({Bclt}*{r}*{r})**2',
                                     ignore_divide_by_zero=True)

    # enable correct blanking for calculating flux
    plot = tp.active_frame().plot()
    plot.value_blanking.active = True
    # blanking of r as done for integration
    run.blanking(0, "r", RelOp.LessThanOrEqual, B_CLT_R_THRESHOLD, active=True)

    # blanking scaled bz sq always active
    run.blanking(3, "scaled_bz_sq", RelOp.LessThan,
                 B_CLT_SCALED_SQ_THRESHOLD, active=True)

    # blanking of bz_eq
    run.blanking(1, "bz_eq", RelOp.LessThan, 0, active=False)
    run.blanking(2, "bz_eq", RelOp.GreaterThan, 0, active=False)

    # set up slice
    # default obey blanking = True
    plot = tp.active_frame().plot()
    plot.slice(0).orientation = SliceSurface.ZPlanes
    plot.slice(0).origin.z = 0

    #! test this
    tp.macro.execute_command(f'$!GlobalTime SolutionTime = 0')

    # extract slices (obey blanking)
    run.timestrands.append("slices_at_equatorial")
    plot.slices(0).extract(
        transient_mode=TransientOperationMode.AllSolutionTimes,
        assign_strand_ids=True
    )
    logger.info(
        "Done extracting slice and setting up time strands.")

    # do integration of flux
    if doPlus:
        ### + side ###
        # 5) Integrate
        run.performIntegration(
            "bz_eq", "Flux", blanking_enable=[1], blanking_disable=[2])
        logger.debug("Done integrating + side.")

        # fix frame
        tp.macro.execute_command('''$!FrameControl ActivateByNumber
            Frame = 2''')
        # tp.active_frame().name = 'plot-plus'
        tp.active_frame().load_stylesheet(
            'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\python scripts\\tecplot-files\\flux_visuals_2.sty')
        run.twoD_plot_fix_axesOnly()
        setup_border_size_position_frame((1, 0.25))

        tp.export.save_png(os.path.join(run.store_gfx_path, "flux", "tecplot-images",
                                        run.run_name + "-flux-poloidal-plus.png"),
                           width=1200,
                           region=ExportRegion.CurrentFrame,
                           supersample=3,
                           convert_to_256_colors=False)
        # tp.active_page().delete_frame(tp.active_page().frames()[-1])
        logger.debug("Done saving graph + side.")

        # 7) Save data
        tp.macro.execute_extended_command(
            command_processor_id="CFDAnalyzer4",
            command=f"""SaveIntegrationResults
                FileName='{double_slashes(run.store_data_path)}\\\\flux\\\\{run.run_name}-flux-poloidal-plus.txt'""",
        )
        logger.debug("Done saving data + side.")
        logger.info("Done with + side.")

    if doMinus:
        tp.macro.execute_command(
            '''$!FrameControl ActivateByNumber Frame = 1''')

        ### - side ###
        run.performIntegration("bz_eq", "Flux", blanking_enable=[
            2], blanking_disable=[1])

        logger.debug("Done integrating - side.")

        tp.macro.execute_command('''$!FrameControl ActivateByNumber
            Frame = 2''')
        # tp.active_frame().name = 'plot-minus'
        tp.active_frame().load_stylesheet(
            'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\python scripts\\tecplot-files\\flux_visuals_2.sty')
        run.twoD_plot_fix_axesOnly()
        setup_border_size_position_frame((1, 2.25))

        tp.export.save_png(os.path.join(run.store_gfx_path, "flux", "tecplot-images",
                                        run.run_name + "-flux-poloidal-minus.png"),
                           width=1200,
                           region=ExportRegion.CurrentFrame,
                           supersample=3,
                           convert_to_256_colors=False)
        # tp.active_page().delete_frame(tp.active_page().frames()[-1])
        logger.debug("Done saving graph - side.")

        # 7) Save data
        tp.macro.execute_extended_command(
            command_processor_id="CFDAnalyzer4",
            command=f"""SaveIntegrationResults
                FileName='{double_slashes(run.store_data_path)}\\\\flux\\\\{run.run_name}-flux-poloidal-minus.txt'""",
        )
        logger.debug("Done saving data - side.")
        logger.info("Done with - side.")

    # visualize as you want
    tp.macro.execute_command(
        """$!FrameControl ActivateByNumber Frame = 1""")
    # view angle
    setup_view_angle_XY()

    # disable shades created by extracting slices
    plot.show_shade = False

    # fix slices
    plot.show_slices = True

    # slice 0: with blanking
    plot.slice(0).show = True
    plot.slice(0).contour.flood_contour_group_index = 0
    plot.slice(0).orientation = SliceSurface.ZPlanes
    plot.slice(0).origin.z = 0

    # slice 1: without blanking
    plot.slice(1).show = True
    plot.slice(1).contour.flood_contour_group_index = 0
    plot.slice(1).orientation = SliceSurface.ZPlanes
    plot.slice(1).origin.z = 0
    plot.slice(1).obey_source_zone_blanking = False
    plot.slice(1).effects.use_translucency = True
    plot.slice(1).effects.surface_translucency = 90

    # contour
    plot.contour(0).variable = run.layout.variable("bz_eq")
    plot.contour(0).levels.reset_levels([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
    plot.contour(0).colormap_name = 'Diverging - Blue/Red'
    plot.contour(0).legend.box.box_type = tp.constant.TextBox.None_

    # fix frames, location and style
    # see after integration

    # blanking
    # r blanking enabled
    tp.active_frame().plot().value_blanking.constraint(0).active = True
    # bz blanking disabled
    tp.active_frame().plot().value_blanking.constraint(1).active = False
    tp.active_frame().plot().value_blanking.constraint(2).active = False
    # bz_above_or_below blanking enabled
    tp.active_frame().plot().value_blanking.constraint(3).active = True

    # export png or animation
    tp.macro.execute_command(f'$!GlobalTime SolutionTime = 0')
    tp.macro.execute_command('$!RedrawAll')
    tp.export.save_time_animation_mpeg4(
        os.path.join(run.store_gfx_path, "flux", "movies",
                     "animation" + run_name[-3:] + ".mp4"),
        start_time=0,
        end_time=len(run),
        timestep_step=1,
        width=1400,
        animation_speed=10,
        region=ExportRegion.AllFrames,
        supersample=3
    )
    logger.debug("Done exporting movie.")

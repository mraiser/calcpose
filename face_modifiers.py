def list_all():
    modifiers = [
                 'head/head-diamond',
                 'head/head-invertedtriangular',
                 'head/head-oval',
                 'head/head-rectangular',
                 'head/head-round',
                 'head/head-square',
                 'head/head-triangular',
                 'head/head-scale-depth-decr|incr',
                 'head/head-scale-horiz-decr|incr',
                 'head/head-scale-vert-decr|incr',
                 'head/head-trans-backward|forward',
                 'head/head-trans-down|up',
                 'head/head-trans-in|out',
                 'head/head-angle-in|out',
                 'head/head-back-scale-depth-decr|incr',
                 'head/head-fat-decr|incr',
                 'head/head-age-decr|incr',
                 'forehead/forehead-nubian-decr|incr',
                 'forehead/forehead-scale-vert-decr|incr',
                 'forehead/forehead-temple-decr|incr',
                 'forehead/forehead-trans-backward|forward',
                 'cheek/l-cheek-bones-decr|incr',
                 'cheek/l-cheek-inner-decr|incr',
                 'cheek/l-cheek-trans-down|up',
                 'cheek/l-cheek-volume-decr|incr',
                 'cheek/r-cheek-bones-decr|incr',
                 'cheek/r-cheek-inner-decr|incr',
                 'cheek/r-cheek-trans-down|up',
                 'cheek/r-cheek-volume-decr|incr',
                 'chin/chin-bones-decr|incr',
                 'chin/chin-cleft-decr|incr',
                 'chin/chin-height-decr|incr',
                 'chin/chin-jaw-drop-decr|incr',
                 'chin/chin-prognathism-decr|incr',
                 'chin/chin-prominent-decr|incr',
                 'chin/chin-width-decr|incr',
                 'ears/l-ear-flap-decr|incr',
                 'ears/l-ear-lobe-decr|incr',
                 'ears/l-ear-rot-backward|forward',
                 'ears/l-ear-scale-decr|incr',
                 'ears/l-ear-scale-depth-decr|incr',
                 'ears/l-ear-scale-vert-decr|incr',
                 'ears/l-ear-shape-pointed|triangle',
                 'ears/l-ear-shape-square|round',
                 'ears/l-ear-trans-backward|forward',
                 'ears/l-ear-trans-down|up',
                 'ears/l-ear-wing-decr|incr',
                 'ears/r-ear-flap-decr|incr',
                 'ears/r-ear-lobe-decr|incr',
                 'ears/r-ear-rot-backward|forward',
                 'ears/r-ear-scale-decr|incr',
                 'ears/r-ear-scale-depth-decr|incr',
                 'ears/r-ear-scale-vert-decr|incr',
                 'ears/r-ear-shape-pointed|triangle',
                 'ears/r-ear-shape-square|round',
                 'ears/r-ear-trans-backward|forward',
                 'ears/r-ear-trans-down|up',
                 'ears/r-ear-wing-decr|incr',
                 'eyebrows/eyebrows-angle-down|up',
                 'eyebrows/eyebrows-trans-backward|forward',
                 'eyebrows/eyebrows-trans-down|up',
                 'eyes/l-eye-bag-decr|incr',
                 'eyes/l-eye-bag-height-decr|incr',
                 'eyes/l-eye-bag-in|out',
                 'eyes/l-eye-corner1-down|up',
                 'eyes/l-eye-corner2-down|up',
                 'eyes/l-eye-epicanthus-in|out',
                 'eyes/l-eye-eyefold-angle-down|up',
                 'eyes/l-eye-eyefold-concave|convex',
                 'eyes/l-eye-eyefold-down|up',
                 'eyes/l-eye-height1-decr|incr',
                 'eyes/l-eye-height2-decr|incr',
                 'eyes/l-eye-height3-decr|incr',
                 'eyes/l-eye-push1-in|out',
                 'eyes/l-eye-push2-in|out',
                 'eyes/l-eye-scale-decr|incr',
                 'eyes/l-eye-trans-down|up',
                 'eyes/l-eye-trans-in|out',
                 'eyes/r-eye-bag-decr|incr',
                 'eyes/r-eye-bag-height-decr|incr',
                 'eyes/r-eye-bag-in|out',
                 'eyes/r-eye-corner1-down|up',
                 'eyes/r-eye-corner2-down|up',
                 'eyes/r-eye-epicanthus-in|out',
                 'eyes/r-eye-eyefold-angle-down|up',
                 'eyes/r-eye-eyefold-concave|convex',
                 'eyes/r-eye-eyefold-down|up',
                 'eyes/r-eye-height1-decr|incr',
                 'eyes/r-eye-height2-decr|incr',
                 'eyes/r-eye-height3-decr|incr',
                 'eyes/r-eye-push1-in|out',
                 'eyes/r-eye-push2-in|out',
                 'eyes/r-eye-scale-decr|incr',
                 'eyes/r-eye-trans-down|up',
                 'eyes/r-eye-trans-in|out',
                 'mouth/mouth-angles-down|up',
                 'mouth/mouth-cupidsbow-decr|incr',
                 'mouth/mouth-cupidsbow-width-decr|incr',
                 'mouth/mouth-dimples-in|out',
                 'mouth/mouth-laugh-lines-in|out',
                 'mouth/mouth-lowerlip-ext-down|up',
                 'mouth/mouth-lowerlip-height-decr|incr',
                 'mouth/mouth-lowerlip-middle-down|up',
                 'mouth/mouth-lowerlip-volume-decr|incr',
                 'mouth/mouth-lowerlip-width-decr|incr',
                 'mouth/mouth-philtrum-volume-decr|incr',
                 'mouth/mouth-scale-depth-decr|incr',
                 'mouth/mouth-scale-horiz-decr|incr',
                 'mouth/mouth-scale-vert-decr|incr',
                 'mouth/mouth-trans-backward|forward',
                 'mouth/mouth-trans-down|up',
                 'mouth/mouth-trans-in|out',
                 'mouth/mouth-upperlip-ext-down|up',
                 'mouth/mouth-upperlip-height-decr|incr',
                 'mouth/mouth-upperlip-middle-down|up',
                 'mouth/mouth-upperlip-volume-decr|incr',
                 'mouth/mouth-upperlip-width-decr|incr',
                 'nose/nose-base-down|up',
                 'nose/nose-compression-compress|uncompress',
                 'nose/nose-curve-concave|convex',
                 'nose/nose-flaring-decr|incr',
                 'nose/nose-greek-decr|incr',
                 'nose/nose-hump-decr|incr',
                 'nose/nose-nostrils-angle-down|up',
                 'nose/nose-nostrils-width-decr|incr',
                 'nose/nose-point-down|up',
                 'nose/nose-point-width-decr|incr',
                 'nose/nose-scale-depth-decr|incr',
                 'nose/nose-scale-horiz-decr|incr',
                 'nose/nose-scale-vert-decr|incr',
                 'nose/nose-septumangle-decr|incr',
                 'nose/nose-trans-backward|forward',
                 'nose/nose-trans-down|up',
                 'nose/nose-trans-in|out',
                 'nose/nose-volume-decr|incr',
                 'nose/nose-width1-decr|incr',
                 'nose/nose-width2-decr|incr',
                 'nose/nose-width3-decr|incr']
    return modifiers

# Chapter 6: Runtime View

## Scenario 1: Successful Command Execution

```
Controller -> CLI       : "FFRFF"
CLI        -> Parser    : parse("FFRFF")
Parser     -> Engine    : [Forward, Forward, Right, Forward, Forward]
Engine     -> Grid      : check_boundary(x, y)
Grid       -> Engine    : ok
Engine     -> CLI       : RoverState(x=2, y=2, heading=E)
CLI        -> Controller: "(2, 2, E)"
```

## Scenario 2: Obstacle Detected

```
Controller -> CLI    : "FFF"
CLI        -> Parser : parse("FFF")
Parser     -> Engine : [Forward, Forward, Forward]
Engine     -> Grid   : check_boundary(0, 2)
Grid       -> Engine : obstacle at (0, 2)
Engine     -> CLI    : ObstacleError(last_safe=(0, 1))
CLI        -> Controller: "Obstacle at (0, 2), stopped at (0, 1)"
```

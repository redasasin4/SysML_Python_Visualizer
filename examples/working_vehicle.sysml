package VehicleExample {
    part def Vehicle {
        part engine : Engine;
        part wheels : Wheel[4];
        part body : Body;
        perform Vehicle_Action;
    }
    action Vehicle_Action{
        action Engine_Action;
    }
    part def Engine {
        perform Vehicle_Action.Engine_Action;
    }

    part def Wheel {
    }

    part def Body {
    }

    part myVehicle : Vehicle;
}
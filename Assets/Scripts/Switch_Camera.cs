using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Switch_Camera : MonoBehaviour
{
    public static int camera_pos = 1;
    void OnMouseDown() {
        if (camera_pos == 1) {
            camera_pos = 2;
        } else {
            camera_pos = 1;
        }
    }
}

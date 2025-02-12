using System.Collections;
using System.Collections.Generic;
using System.Numerics;
using UnityEngine;

public class Edit_Position : MonoBehaviour
{
    
    void Update()
    {
       if (Switch_Camera.camera_pos == 1) {
            transform.position = new UnityEngine.Vector3(50.75f,2.19f,50f);
            transform.localRotation = UnityEngine.Quaternion.Euler(0f, 0f, 0f);
       } else if (Switch_Camera.camera_pos == 2) {
            transform.position = new UnityEngine.Vector3(50.75f,2.19f,50f);
            transform.localRotation = UnityEngine.Quaternion.Euler(0f, -90f, 0f);
       } else {
            transform.position = new UnityEngine.Vector3(100f,100f,100f);
       }
    }
    
}

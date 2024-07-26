using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Edit_Position : MonoBehaviour
{
    
    void Update()
    {
       if (Switch_Camera.camera_pos == 1) {
            transform.localRotation = Quaternion.Euler(0f, 0f, 0f);
       } else {
            
            transform.localRotation = Quaternion.Euler(0f, -90f, 0f);
       }
    }
    
}

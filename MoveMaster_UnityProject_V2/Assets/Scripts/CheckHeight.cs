using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CheckHeight : MonoBehaviour
{
    public GameObject plane;
    public Camera m_camera;

    void Start()
    {
        plane = GameObject.Find("Plane");
        m_camera = Camera.main;
    }

    void Update()
    {
        if (plane != null)
        {
            float currentY = plane.transform.position.y;
            float diff = currentY - 8.275f;
            int count = 0;

            while (diff > 0)
            {
                diff -= 0.48f;
                count++;
            }

            m_camera.orthographicSize = 4.5f + (0.5f * count);
        }
        else
        {
            Debug.LogError("Plane GameObject not found!");
        }
    }
}

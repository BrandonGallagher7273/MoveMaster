using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CheckHeight : MonoBehaviour
{
    public GameObject plane;
    public Camera m_camera;
    private float targetSize;
    private float zoomVelocity = 0f; // Used for SmoothDamp

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

            // Compute the target size
            targetSize = 4.5f + (0.00025f * count);

            // Smoothly interpolate using SmoothDamp
            m_camera.orthographicSize = Mathf.SmoothDamp(m_camera.orthographicSize, targetSize, ref zoomVelocity, 0.5f);
            m_camera.transform.position = new Vector3(m_camera.transform.position.x,Mathf.SmoothDamp(m_camera.transform.position.y, m_camera.transform.position.y+(0.45f*count), ref zoomVelocity, 0.7f),m_camera.transform.position.z);
        }
        else
        {
            Debug.LogError("Plane GameObject not found!");
        }
    }
}

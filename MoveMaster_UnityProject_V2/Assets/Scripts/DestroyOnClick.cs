using System;
using UnityEngine;

public class DestroyOnClick : MonoBehaviour
{
    public GameObject player;
    public GameObject valid_checker;
    public Camera mainCamera;
    public GameObject plane;

    private static GameObject selectedBlock = null;
    private static bool waitingForPlaneClick = false;
    public static bool started = false;
    private static bool wasStarted = false;

    private Vector3 leftPosition;
    private Vector3 middlePosition;
    private Vector3 rightPosition;

    private static bool leftOccupied = false;
    private static bool middleOccupied = false;
    private static bool rightOccupied = false;
    private static int placedCount = 0;
    private static bool isVertical = false;

    private float planeHeightIncrement = 0.48f;
    private Vector3 initialPlanePosition = new Vector3(50.75f, 8.275f, 50f);

    void Start()
    {
        player = GameObject.Find("Player");
        valid_checker = GameObject.Find("Valid_Check");

        if (mainCamera == null)
        {
            mainCamera = Camera.main;
        }

        ResetSimulation();
    }

    void Update()
    {
        if (wasStarted && !started)
        {
            ResetSimulation();
        }

        wasStarted = started;

        if (waitingForPlaneClick && Input.GetMouseButtonDown(0))
        {
            Ray ray = mainCamera.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit) && hit.collider.gameObject == plane)
            {
                if (selectedBlock != null)
                {
                    Vector3 targetPosition = GetClosestPosition(hit.point);
                    targetPosition.y = plane.transform.position.y + 0.05f;

                    if (targetPosition == leftPosition && leftOccupied ||
                        targetPosition == middlePosition && middleOccupied ||
                        targetPosition == rightPosition && rightOccupied)
                    {
                        Debug.Log("This position is already occupied!");
                        return;
                    }

                    Debug.Log("Placing block at: " + targetPosition);
                    selectedBlock.transform.position = targetPosition;
                    selectedBlock.transform.rotation = Quaternion.Euler(0, isVertical ? 90 : 0, 0);
                    selectedBlock.SetActive(true);

                    if (targetPosition == leftPosition) leftOccupied = true;
                    if (targetPosition == middlePosition) middleOccupied = true;
                    if (targetPosition == rightPosition) rightOccupied = true;

                    placedCount++;
                    if (placedCount == 3)
                    {
                        Debug.Log("3 placed! Raising plane.");
                        RaisePlane();
                    }

                    selectedBlock = null;
                    waitingForPlaneClick = false;
                }
            }
        }
    }

    private void OnMouseDown()
    {
        if (!started && !waitingForPlaneClick && selectedBlock == null)
        {
            selectedBlock = gameObject;
            Debug.Log("Block selected: " + selectedBlock.name);
            selectedBlock.SetActive(false);
            waitingForPlaneClick = true;
        }
    }

    private Vector3 GetClosestPosition(Vector3 clickedPos)
    {
        Vector3 closest = leftPosition;
        float minDistance = Vector3.Distance(clickedPos, leftPosition);

        if (Vector3.Distance(clickedPos, middlePosition) < minDistance)
        {
            closest = middlePosition;
            minDistance = Vector3.Distance(clickedPos, middlePosition);
        }

        if (Vector3.Distance(clickedPos, rightPosition) < minDistance)
        {
            closest = rightPosition;
        }

        return closest;
    }

    private void RaisePlane()
    {
        plane.transform.position += new Vector3(0, planeHeightIncrement, 0);
        isVertical = !isVertical;
        SetPlacementPositions();
        leftOccupied = false;
        middleOccupied = false;
        rightOccupied = false;
        placedCount = 0;
    }

    private void SetPlacementPositions()
    {
        if (isVertical)
        {
            leftPosition = new Vector3(50.75f, plane.transform.position.y + 0.05f, 49.25f);
            middlePosition = new Vector3(50.75f, plane.transform.position.y + 0.05f, 50f);
            rightPosition = new Vector3(50.75f, plane.transform.position.y + 0.05f, 50.75f);
        }
        else
        {
            leftPosition = new Vector3(50f, plane.transform.position.y + 0.05f, 50f);
            middlePosition = new Vector3(50.75f, plane.transform.position.y + 0.05f, 50f);
            rightPosition = new Vector3(51.5f, plane.transform.position.y + 0.05f, 50f);
        }
    }

    private void ResetSimulation()
    {
        plane.transform.position = initialPlanePosition;
        isVertical = false;
        leftOccupied = false;
        middleOccupied = false;
        rightOccupied = false;
        placedCount = 0;
        SetPlacementPositions();
        Debug.Log("Simulation Reset");
    }
}

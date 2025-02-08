using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TowerReset : MonoBehaviour
{
    public GameObject player;
    public GameObject valid_checker;

    void Start() {
        player = GameObject.Find("Player");
        valid_checker = GameObject.Find("Valid_Check");
    }

    void OnMouseDown() {
        if (DestroyOnClick.started == false) {
            BlockPlacement bc_1 = player.GetComponent<BlockPlacement>();
            bc_1.SpawnBlocks();
            DetectFall fall = valid_checker.GetComponent<DetectFall>();
            fall.ChangeMat(1);
        }
    }
}

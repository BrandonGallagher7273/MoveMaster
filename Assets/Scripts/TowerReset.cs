using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TowerReset : MonoBehaviour
{
    public GameObject player;

    void Start() {
        player = GameObject.Find("Player");
    }

    void OnMouseDown() {
        if (DestroyOnClick.started == false) {
            BlocksCopy bc_1 = player.GetComponent<BlocksCopy>();
            bc_1.ResetSpawnCode_l();
            BlocksCopy_4 bc_2 = player.GetComponent<BlocksCopy_4>();
            bc_2.ResetSpawnCode_r();
        }
    }
}
